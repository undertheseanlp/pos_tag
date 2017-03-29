# -*- coding: utf-8 -*-
from os.path import dirname, join
import lxml.etree as ET
import pandas as pd
from underthesea.corpus import PlainTextCorpus

raw_folder = dirname(__file__)
corpus = PlainTextCorpus()
corpus.load(join(dirname(dirname(dirname(__file__))), "data", "raw"))
sentences = [sentence for document in corpus.documents for sentence in document.sentences]
total_sentences = len(sentences)
words = [token for sentence in sentences for token in sentence.split(" ")]
total_words = len(words)
total_tokens = total_words
total_fused = 0

report_file = dirname(dirname(__file__))
root = ET.Element('treebank')
comment = ET.Comment(u""" tokens means "surface tokens", e.g. Spanish "vámonos" counts as one token
       words means "syntactic words", e.g. Spanish "vámonos" is split to two words, "vamos" and "nos"
       fused is the number of tokens that are split to two or more syntactic words
       The words and fused elements can be omitted if no token is split to smaller syntactic words.""")
root.append(comment)

size = ET.SubElement(root, 'size')
total = ET.SubElement(size, 'total')
sentences = ET.SubElement(total, 'sentences')
sentences.text = str(total_sentences)
words = ET.SubElement(total, 'words')
words.text = str(total_words)
tokens = ET.SubElement(total, 'tokens')
tokens.text = str(total_tokens)
fused = ET.SubElement(total, 'fused')
fused.text = "0"

comment = ET.Comment(u" ., ,, \", và, không, là, có, của, người, một, được, đã, :, ông, ... ")
root.append(comment)
lemmas = ET.SubElement(root, "lemmas", unique="0")
comment = ET.Comment(u" ., ,, \", và, không, là, có, của, người, một, được, đã, :, ông, ... ")
root.append(comment)
forms = ET.SubElement(root, "forms", unique="0")
comment = ET.Comment(u" ")
root.append(comment)
fusions = ET.SubElement(root, "fusions", unique="0")

comment = ET.Comment(
    u" Statistics of universal POS tags. The comments with the most frequent lemmas are optional (but easy to obtain). ")
root.append(comment)
tags = ET.SubElement(root, "tags", unique="0")

tree = ET.ElementTree(root)
tree.write("stats.xml", pretty_print=True, xml_declaration=True, encoding='utf-8')
