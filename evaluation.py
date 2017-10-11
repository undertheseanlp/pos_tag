# -*- coding: utf-8 -*-
from difflib import ndiff, unified_diff, context_diff
from os import listdir, mkdir
import shutil
from os.path import dirname, join, isfile
from underthesea.util.file_io import read, write
from models.pos_tag_1 import pos_tag


def load_input(input_file):
    lines = read(input_file).strip().split("\n")
    content = [line.split("\t")[0] for line in lines]
    content = u" ".join(content)
    return content


def load_output(input_file):
    text = read(input_file)
    return text


def convert_output_to_text(output):
    text = u"\n".join([u"\t".join(item) for item in output])
    return text


def save_temp(id, output):
    test_dir = join(dirname(__file__), "samples", "accuracy")
    temp_file = join(test_dir, "%s.tmp" % id)
    content = u"\n".join(output)
    write(temp_file, content)


def _save_tmp_model(model_id, file_id, output):
    test_dir = join(dirname(__file__), "test_set", model_id)
    temp_file = join(test_dir, "%s.actual" % file_id)
    content = u"\n".join(output)
    write(temp_file, content)


def _compare_model(id1, id2):
    fails1 = listdir(join(dirname(__file__), "test_set", id1))
    fails2 = listdir(join(dirname(__file__), "test_set", id2))
    new_fails = set(fails2) - set(fails1)
    new_improvements = set(fails1) - set(fails2)
    if len(new_fails):
        print("New fails:", new_fails)
    if len(new_improvements):
        print("New improvements:", new_improvements)


def _test_model(model_id, func):
    name = func.__module__
    print("\n")
    print(name)
    test_dir = join(dirname(__file__), "test_set")
    files = [f for f in listdir(test_dir) if isfile(join(test_dir, f))]
    ids = sorted([int(f.split(".")[0]) for f in files if ".in" in f])
    fails = []
    try:
        shutil.rmtree(join(test_dir, model_id))
    except:
        pass
    mkdir(join(test_dir, model_id))
    for id in ids:
        input_file = join(test_dir, "%s.in" % id)
        output_file = join(test_dir, "%s.out" % id)
        sentence = load_input(input_file)
        actual = func(sentence)
        expected = load_output(output_file)
        if actual != expected:
            fails.append(str(id))
            _save_tmp_model(model_id, id, actual)
    if int(model_id) > 1:
        _compare_model(str(int(model_id) - 1), model_id)
    n = len(ids)
    correct = n - len(fails)
    print(
        "Accuracy: {:.2f}% ({}/{})".format(correct * 100.0 / n, correct, n))
    print("Fails   :", ", ".join(fails))


if __name__ == '__main__':
    output = pos_tag(
        "Tài xế “phát hoảng” vì số tiền phạt nguội bằng nửa giá trị chiếc xe")
    test_dir = join(dirname(__file__), "test_set")
    files = [f for f in listdir(test_dir) if isfile(join(test_dir, f))]
    model_id = "1"
    try:
        shutil.rmtree(join(test_dir, model_id))
    except:
        pass
    mkdir(join(test_dir, model_id))
    for f in files:
        input = load_input(join(test_dir, f))
        actual = convert_output_to_text(pos_tag(input))
        expected = load_output(join(test_dir, f))
        if actual != expected:
            print("\n{}".format(f))
            diff = '\n'.join(ndiff(expected.splitlines(), actual.splitlines()))
            print(diff)
            write(join(test_dir, model_id, f), actual)
            write(join(test_dir, model_id, f + ".diff"), diff)
