from underthesea import word_tokenize

from .lstm_model import LSTMModel
from .lstm_tagger import LSTMTagger


def pos_tag(sentence, format=None, model_path=None):
    tokens = word_tokenize(sentence.lower())
    tagger = LSTMModel()
    tagger.instance(model_path)
    output = []
    result = tagger.predict(tokens)
    tags = [token[1] for token in result]
    for tag, token in zip(tags, tokens):
        output.append((token, tag))
    if format == "text":
        output = u" ".join(["{}/{}".format(token.replace(" ", "_"), tag) for token, tag in output])
    return output
