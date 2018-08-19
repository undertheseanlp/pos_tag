import torch

from .load_data import load_dataset
from torch import nn, optim


class LSTMTagger(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super(LSTMTagger, self).__init__()
        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)

    def forward(self, sentence):
        embeds = self.word_embeddings(sentence)
        return embeds


tag_to_indx = {}


def prepare_sequence(seq, to_ix):
    global tag_to_indx
    idxs = []
    i = len(tag_to_indx)
    for item in seq:
        if item not in tag_to_indx:
            tag_to_indx[item] = i
            i += 1
        index = to_ix[item]
        idxs.append(index)
    idxs = [to_ix[item] for item in seq]
    return torch.tensor(idxs, dtype=torch.long)


def train(train_path, model_path):
    train_set = []

    train_set += load_dataset(train_path)
    model = LSTMTagger(100, 300)
    loss_function = nn.NLLLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.1)
    for epoch in range(300):
        for sentence in train_set:
            inputs, tags = zip(*sentence)
            taggets = prepare_sequence(tags, to_ix=tag_to_indx)
            # model.zero_grad()
            # loss = loss_function(y_true, y_pred)
            # loss.backward()
            # optimizer.step()
        print(0)
    print("Load data from file", train_path)
