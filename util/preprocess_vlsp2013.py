from os import makedirs, listdir
from os.path import dirname, join
from languageflow.reader.tagged_corpus import TaggedCorpus
import argparse
import re


def preprocess(file):
    sentences = []
    for line in open(file):
        sentence = []
        line = line.strip()
        line = re.sub(r"_+", "_", line)
        if not line:
            continue
        tokens = line.strip().split(" ")
        try:
            for token in tokens:
                if token.startswith("//"):
                    word = "/"
                    tag = token[2:]
                else:
                    word, tag = token.split("/")
                word = word.replace("_", " ")
                sentence.append([word, tag])
        except:
            continue
        sentences.append(sentence)
    return sentences


def raw_to_corpus(sample, output):
    if output:
        output_folder = output
    else:
        output_folder = join(dirname(dirname(__file__)), "tmp", "vlsp2013")
    try:
        makedirs(output_folder)
    except Exception as e:
        pass
    raw_folders = ["Trainset-POS-full", "Testset-POS"]
    output_names = ["train.txt", "test.txt"]
    data_folder = join(dirname(dirname(__file__)), "data", "vlsp2013", "raw")
    for i, raw_folder in enumerate(raw_folders):
        tagged_corpus = TaggedCorpus()
        sentences = []
        files = listdir(join(data_folder, raw_folder))
        files = [join(data_folder, raw_folder, file) for file in files]
        for file in files:
            sentences += preprocess(file)
            if sample != None:
                if len(sentences) > sample:
                    sentences = sentences[:sample]
                    break
        tagged_corpus.sentences = sentences
        output_file = join(output_folder, output_names[i])
        tagged_corpus.save(output_file)
        print("{} sentences is saved to file {}".format(len(sentences), output_file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser("preprocess_vlsp2013.py")
    parser.add_argument("--sample", help="sample size", type=int)
    parser.add_argument("--output", help="output path")
    args = parser.parse_args()
    if args.sample:
        if not args.output:
            parser.error("You must set --output when use option --sample")
    raw_to_corpus(sample=args.sample, output=args.output)
