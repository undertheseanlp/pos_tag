# -*- coding: utf-8 -*-
import pycrfsuite
import time

from datetime import datetime
from underscore import _
from sklearn.metrics import confusion_matrix

from models.crf_model.model_profiling import ModelProfiling
from transformer import sent2labels
from transformer import Transformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def sentence_to_tuple(sentence):
    return [(token.word, token.tags) for token in sentence.words]


def sentence_to_labels(sentence):
    return [token.tags for token in sentence]


def convert_cm_to_log(cm, labels):
    cm = cm.tolist()
    cm = [" ".join(["%-3s" % labels[index]] + map(lambda i: "%3d" % i, row)) for index, row in enumerate(cm)]
    labels = "    " + " ".join(map(lambda i: "%3s" % i, labels))
    cm.insert(0, labels)
    return cm


if __name__ == '__main__':
    transformer = Transformer()
    train_sents = transformer.load_train_sents()
    template = [
        "T[0].lower", "T[-1].lower", "T[1].lower",
        "T[0].istitle", "T[-1].istitle", "T[1].istitle",
        "T[-2]", "T[-1]", "T[0]", "T[1]", "T[2]",  # unigram
        "T[-2,-1]", "T[-1,0]", "T[0,1]", "T[1,2]",  # bigram
        "T[-1][1]", "T[-2][1]", "T[-3][1]",  # dynamic feature
        "T[-3,-2][1]", "T[-2,-1][1]",
        "T[-3,-1][1]"
    ]
    train_sents = [sentence_to_tuple(sentence) for sentence in train_sents]
    X = [Transformer.extract_features(s, template) for s in train_sents]
    y = [sent2labels(s) for s in train_sents]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=10)
    trainer = pycrfsuite.Trainer(verbose=True)
    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)
    model_params = {
        "name": "CRF",
        "params": {
            'c1': 1.0,  # coefficient for L1 penalty
            'c2': 1e-3,  # coefficient for L2 penalty
            'max_iterations': 1000,  #
            # include transitions that are possible, but not observed
            'feature.possible_transitions': True
        }
    }
    trainer.set_params(model_params["params"])
    profile = ModelProfiling()
    profile.add("data", {"train": len(X_train), "test": len(X_test)})
    profile.add("model", model_params)
    profile.add("template", template)

    profile.start_train()
    model_name = "crf-postag-%s" % datetime.now().strftime('%Y-%m-%d_%H-%M')
    trainer.train(model_name)
    profile.end_train()

    model = pycrfsuite.Tagger()
    model.open(model_name)
    y_pred = [model.tag(x) for x in X_test]
    y_test = _.flatten(y_test)
    y_pred = _.flatten(y_pred)
    labels = list(set(y_test).union(set(y_pred)))

    cm = confusion_matrix(y_test, y_pred, labels)
    cm = convert_cm_to_log(cm, labels)
    profile.add("accuracy score", accuracy_score(y_test, y_pred))
    profile.add("confusion matrix", cm)

    profile.save()
    profile.show()
