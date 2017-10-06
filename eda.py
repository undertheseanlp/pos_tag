from os.path import join
from underthesea_flow.reader.tagged_corpus import TaggedCorpus

if __name__ == '__main__':
    total_corpus = TaggedCorpus()
    for file in ["train", "test", "dev"]:
        input_file = join("corpus", "treebank", file + ".txt")
        output_folder = join("eda", "treebank", file)

        corpus = TaggedCorpus()
        corpus.load(input_file)
        total_corpus.sentences += corpus.sentences

        corpus.analyze(output_folder=output_folder, auto_remove=True)
    total_corpus.analyze(output_folder=join("eda", "treebank", "total"))
