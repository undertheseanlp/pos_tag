# Underthesea POS Tagging

![](https://img.shields.io/badge/build-passing-brightgreen.svg) ![](https://img.shields.io/badge/accuracy-92.3%25-red.svg)

This repository contains starter code for training and evaluating machine learning models in *Vietnamese POS Tagging* problem. It is a part of [underthesea](https://github.com/magizbox/underthesea) project. The code gives an end-to-end working example for reading datasets, training machine learning models, and evaluating performance of the models. It can easily be extended to train your own custom-defined models. 

## Table of contents

* [1. Installation](#1-installation)
  * [1.1 Requirements](#11-requirements)
  * [1.2 Download and Setup Environement](#12-download-and-setup-environment)
* [2. Usage](#2-usage)
  * [2.1 Using a pretrained model](#21-using-a-pre-trained-model)
  * [2.2 Train a new dataset](#22-train-a-new-dataset)
* [3. References](#3-references)

## 1. Installation

### 1.1 Requirements

* `Operating Systems: Linux (Ubuntu, CentOS), Mac`
* `Python 3.6`
* `Anaconda`
* `languageflow==1.1.7`

### 1.2 Download and Setup Environment

Clone project using git

```
$ git clone https://github.com/undertheseanlp/pos_tag.git
```

Create environment and install requirements

```
$ cd word_tokenize
$ conda create -n pos_tag python=3.6
$ pip install -r requirements.txt
```

## 2. Usage

Make sure you are in `pos_tag` folder and activate `pos_tag` environment

```
$ cd pos_tag
$ source activate pos_tag
``` 

### 2.2 Train a new dataset

**Train and test**

```
$ python util/preprocess_vlsp2013.py
$ python train.py \
    --train tmp/vlsp2013/train.txt \
    --test tmp/vlsp2013/test.txt
```

Last update: August 2018
