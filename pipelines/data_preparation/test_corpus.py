from os.path import join, dirname
from unittest import TestCase

from pipelines.data_preparation.corpus import TaggedCorpus


class TestTaggedCorpus(TestCase):
    def test_load(self):
        ud_file = join(dirname(dirname(dirname(__file__))), "data", "ud", "vi_ud.conllu")
        tagged_corpus = TaggedCorpus()
        tagged_corpus.load(ud_file)

    def test_sent(self):
        ud_file = join(dirname(dirname(dirname(__file__))), "data", "ud", "vi_ud.conllu")
        tagged_corpus = TaggedCorpus()
        tagged_corpus.load(ud_file)
        sentences = tagged_corpus.sents()
        self.assertGreater(len(sentences), 10)
