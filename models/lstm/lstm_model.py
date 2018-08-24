from os.path import join, dirname
import joblib
import torch

from .train import _category_from_output
from .util import IndexUtil
from .lstm_tagger import LSTMTagger


class LSTMModel:
    objects = {}

    def __init__(self, model_path=None):
        if not model_path:
            model_path = join(dirname(__file__), "model.lstm.bin")
        metadata = joblib.load(join(dirname(__file__), "metadata.bin"))
        params = metadata["params"]
        tagger = LSTMTagger(hidden_dim=params["hidden_dim"],
                            embedding_dim=params["embedding_dim"],
                            vocab_size=params["vocab_size"],
                            tags_size=params["tags_size"])
        tagger.load_state_dict(torch.load(model_path))
        self.metadata = metadata
        self.tagger = tagger

    @classmethod
    def instance(cls, model_path=None):
        if model_path not in cls.objects:
            cls.objects[model_path] = cls(model_path)
        object = cls.objects[model_path]
        return object

    def predict(self, tokens, format=None):
        words_to_indexes = self.metadata["words_to_indexes"]
        input = IndexUtil.get_tokens_to_indexes(words_to_indexes, tokens)
        input = torch.LongTensor(input)
        self.tagger = self.tagger.cuda()
        scores = self.tagger(input).cpu()
        tags = _category_from_output(scores, self.metadata["indexes_to_tags"])
        return list(zip(tokens, tags))
