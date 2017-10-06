# POS Tagging Experiments

This repository contains experiments in Vietnamese POS Tagging problems. It is a part of [underthesea](https://github.com/magizbox/underthesea) project.

## Corpus Summary 

Corpus is in [UniversalDependencies format](https://github.com/UniversalDependencies/UD_Vietnamese).

```
Sentences    : 16281
Unique words : 19742
Top words    : ,, ., của, ", là, và, một, có, được, người, không, đã, cho, những, :, -, “, ..., ”, ở
Pos Tags (29): A, Ab, B, C, CH, Cb, Cc, E, Eb, I, L, M, Mb, N, Nb, Nc, Np, Nu, Ny, P, Pb, R, T, V, Vb, Vy, X, Y, Z
```
## Reports

![](https://img.shields.io/badge/accuracy-92.3%25-red.svg)

* [Detail Reports](https://docs.google.com/spreadsheets/d/1nH9XKXzdDWVpJO8uPFjtikL9zJCdZSIxWQX9fqEFmtM/edit?usp=sharing)

## Usage

**Setup Environment**

```
# clone project
$ git clone git@github.com:magizbox/underthesea.pos_tag.git

# create environment
$ cd underthesea.pos_tag
$ conda create -n underthesea.pos_tag python=3.4
$ pip install -r requirement.txt
```

**Run experiment**

```
$ source activate underthesea.pos_tag
$ cd underthesea.chunking
$ python main.py
```
## Related Works

* [Vietnamese POS Tagging Tools](https://github.com/magizbox/underthesea/wiki/Vietnamese-NLP-Tools#part-of-speech-tagging)
* [Vietnamese POS Tagging Publications](https://github.com/magizbox/underthesea/wiki/Vietnamese-NLP-Publications#part-of-speech-tagging)
* [Vietnamese POS Tagging State of The Art](https://github.com/magizbox/underthesea/wiki/Vietnamese-NLP-SOTA#part-of-speech-tagging)
* [Vietnamese POS Tagging Service](https://github.com/magizbox/underthesea/wiki/Vietnamese-NLP-Services#part-of-speech-tagging)

Last update: October 2017
