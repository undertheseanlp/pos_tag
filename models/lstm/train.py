import torch

from models.lstm.lstm_tagger import LSTMTagger
from .load_data import load_dataset
from torch import nn, optim
import joblib

use_gpu = torch.cuda.is_available()


def prepare_sequence(sequence, to_ix):
    idxs = [to_ix[item] for item in sequence]
    return torch.tensor(idxs, dtype=torch.long)


def extract_indexes(train_set):
    tags_to_indexes = {
        "<UNK>": 0
    }
    words_to_indexes = {
        "<UNK>": 0
    }
    w_i = 1
    t_i = 1
    for sentence in train_set:
        words, tags = zip(*sentence)
        for word in words:
            word = word.lower()
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
    metadata = {}
    words_to_indexes, tags_to_indexes = extract_indexes(dataset)
    metadata["words_to_indexes"] = words_to_indexes
    metadata["tags_to_indexes"] = tags_to_indexes
    metadata["indexes_to_tags"] = _reverse_dict(tags_to_indexes)
    indexes_to_tags = _reverse_dict(tags_to_indexes)
    params = {}
    params["hidden_dim"] = 200
    params["embedding_dim"] = 100
    params["vocab_size"] = len(words_to_indexes)
    params["tags_size"] = len(tags_to_indexes)
    metadata["params"] = params
    model = LSTMTagger(hidden_dim=params["hidden_dim"],
                       embedding_dim=params["embedding_dim"],
                       vocab_size=params["vocab_size"],
                       tags_size=params["tags_size"])
    model = model.cuda()

    loss_function = nn.NLLLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
    n_epoch = 10

    train_size = 0.9
    n = int(train_size * len(dataset))
    train_set, test_set = dataset[:n], dataset[n:]
    for epoch in range(n_epoch):
        for sentence in train_set:
            words, tags = zip(*sentence)
            words = [word.lower() for word in words]
            words_indexes = prepare_sequence(words, to_ix=words_to_indexes)
            tags_indexes_true = prepare_sequence(tags, to_ix=tags_to_indexes)
            if use_gpu:
                tags_indexes_true = tags_indexes_true.cuda()

            model.zero_grad()

            model.hidden = model.init_hidden()
            tags_indexes_predict = model(words_indexes)
            loss = loss_function(tags_indexes_predict, tags_indexes_true)
            loss.backward()
            print(loss)
            optimizer.step()
        print("Epoch: {}/{}".format(epoch + 1, n_epoch))

    with torch.no_grad():
        for sentence in test_set:
            words, tags_true = zip(*sentence)
            words = [word.lower() for word in words]
            words_indexes = prepare_sequence(words, to_ix=words_to_indexes)
            tags_indexs_true = prepare_sequence(tags, to_ix=tags_to_indexes)

            tags_scores = model(words_indexes)
            tags_scores = tags_scores.cpu()
            tags_predict = _category_from_output(tags_scores, indexes_to_tags)
            if len(set(tags_predict)) > 1:
                print(list(zip(words, tags_true, tags_predict)))
    torch.save(model.state_dict(), model_path)
    joblib.dump(metadata, "metadata.bin")
    print(0)
