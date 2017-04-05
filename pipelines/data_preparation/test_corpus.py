from os.path import join, dirname
from unittest import TestCase, skip

from pipelines.data_preparation.corpus import TaggedCorpus


class TestTaggedCorpus(TestCase):
    @skip
    def test_load(self):
        ud_file = join(dirname(dirname(dirname(__file__))), "data", "ud", "vi_ud.conllu")
        tagged_corpus = TaggedCorpus()
        tagged_corpus.load(ud_file)
    @skip
    def test_sents_1(self):
        ud_file = join(dirname(dirname(dirname(__file__))), "data", "ud", "vi_ud.conllu")
        tagged_corpus = TaggedCorpus()
        tagged_corpus.load(ud_file)
        sentences = tagged_corpus.sents()
        self.assertGreater(len(sentences), 10)

    def test_sents_2(self):
        ud_file = join("sample", "sample_vi_ud.conllu")
        tagged_corpus = TaggedCorpus()
        tagged_corpus.load(ud_file)
        sents = tagged_corpus.sents()
        self.assertGreater(len(sents), 10)

    def test_words(self):
        ud_file = join("sample", "sample_vi_ud.conllu")
        tagged_corpus = TaggedCorpus()
        tagged_corpus.load(ud_file)
        words = tagged_corpus.words()
        self.assertGreater(len(words), 5000)

    def test_analyze(self):
        ud_file = join("sample", "sample_vi_ud.conllu")
        corpus = TaggedCorpus()
        corpus.load(ud_file)
        data = corpus.analyze()
        self.assertGreater(data["total_words"], 5000)
