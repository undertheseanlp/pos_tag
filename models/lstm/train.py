import torch

from .load_data import load_dataset
from torch import nn, optim
import torch.nn.functional as F


class LSTMTagger(nn.Module):
    def __init__(self, hidden_dim, tags_size):
        super(LSTMTagger, self).__init__()
        self.hidden_dim = hidden_dim
        self.lstm = nn.LSTM(1, self.hidden_dim)

        self.hidden2tag = nn.Linear(hidden_dim, tags_size)
        self.hidden = self.init_hidden()

    def init_hidden(self):
        return (torch.zeros(1, 1, self.hidden_dim),
                torch.zeros(1, 1, self.hidden_dim))

    def forward(self, sentence):
        input = sentence.view(len(sentence), 1, -1).float()
        lstm_out, self.hidden = self.lstm(input, self.hidden)
        tag_space = self.hidden2tag(lstm_out.view(len(sentence), -1))
        tag_scores = F.log_softmax(tag_space, dim=1)
        return tag_scores


def prepare_sequence(sequence, to_ix):
    idxs = [to_ix[item] for item in sequence]
    return torch.tensor(idxs, dtype=torch.long)


def extract_indexes(train_set):
    tags_to_indexes = {}
    words_to_indexes = {}
    w_i = 0
    t_i = 0
    for sentence in train_set:
        words, tags = zip(*sentence)
        for word in words:
            if word not in words_to_indexes:
                words_to_indexes[word] = w_i
                w_i += 1
        for tag in tags:
            if tag not in tags_to_indexes:
                tags_to_indexes[tag] = t_i
                t_i += 1
    return words_to_indexes, tags_to_indexes


def _category_from_output(scores, indexes_to_values):
    top_n, top_i = scores.topk(1)
    indexes = list(top_i.view(-1).numpy())
    values = [indexes_to_values[i] for i in indexes]
    return values


def _reverse_dict(dict):
    return {v: k for k, v in dict.items()}


def train(train_path, model_path):
    dataset = load_dataset(train_path)
    words_to_indexes, tags_to_indexes = extract_indexes(dataset)
    indexes_to_tags = _reverse_dict(tags_to_indexes)

    model = LSTMTagger(hidden_dim=10, tags_size=len(tags_to_indexes))

    loss_function = nn.NLLLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.1)
    n_epoch = 300

    train_size = 0.9
    n = int(train_size * len(dataset))
    train_set, test_set = dataset[:n], dataset[n:]
    for epoch in range(n_epoch):
        for sentence in train_set:
            words, tags = zip(*sentence)
            words_indexes = prepare_sequence(words, to_ix=words_to_indexes)
            tags_indexes_true = prepare_sequence(tags, to_ix=tags_to_indexes)

            model.zero_grad()

            model.hidden = model.init_hidden()
            tags_indexes_predict = model(words_indexes)
            loss = loss_function(tags_indexes_predict, tags_indexes_true)
            loss.backward()
            print(loss)
            optimizer.step()
        print("Epoch: {}/{}".format(epoch + 1, n_epoch))
    print("Load data from file", train_path)

    with torch.no_grad():
        for sentence in test_set:
            words, tags_true = zip(*sentence)
            words_indexes = prepare_sequence(words, to_ix=words_to_indexes)
            tags_indexs_true = prepare_sequence(tags, to_ix=tags_to_indexes)

            tags_scores = model(words_indexes)
            tags_predict = _category_from_output(tags_scores, indexes_to_tags)
            if len(set(tags_predict)) > 1:
                print(list(zip(words,tags_true, tags_predict)))
    print(0)
