from underthesea import word_tokenize

from util.crf.pos_tag.model import CRFModel


def pos_tag(sentence, format=None, model_path=None):
    tokens = word_tokenize(sentence)
    model = CRFModel.instance(model_path)
    output = model.predict(tokens)
    tokens = [token[0] for token in output]
    tags = [token[1] for token in output]
    output = []
    for tag, token in zip(tags, tokens):
        output.append((token, tag))
    if format == "text":
        output = u" ".join(["{}/{}".format(token.replace(" ", "_"), tag) for token, tag in output])
    return output


if __name__ == '__main__':
    output = pos_tag("Đang họp báo vụ điểm cao bất thường ở Sơn La", format="text")
    print(output)
