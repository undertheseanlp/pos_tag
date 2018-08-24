import torch
import torch.nn.functional as F
from torch import nn

use_gpu = torch.cuda.is_available()


class LSTMTagger(nn.Module):
    def __init__(self, hidden_dim, embedding_dim, vocab_size, tags_size):
        super(LSTMTagger, self).__init__()
        self.hidden_dim = hidden_dim
        self.embedding_dim = embedding_dim
        self.vocab_size = vocab_size

        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, self.hidden_dim, bidirectional=True)

        self.hidden2tag = nn.Linear(hidden_dim * 2, tags_size)
        self.hidden = self.init_hidden()

    def init_hidden(self):
        hiddens = (torch.zeros(2, 1, self.hidden_dim).cuda(),
                torch.zeros(2, 1, self.hidden_dim).cuda())
        return hiddens

    def forward(self, sentence):
        embeds = self.word_embeddings(sentence.cuda())
        lstm_out, self.hidden = self.lstm(
            embeds.view(len(sentence), 1, -1),
            self.hidden)
        tag_space = self.hidden2tag(lstm_out.view(len(sentence), -1))
        tag_scores = F.log_softmax(tag_space, dim=1)
        return tag_scores
