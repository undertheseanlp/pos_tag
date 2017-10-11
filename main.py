from os.path import dirname, join
from underthesea_flow.flow import Flow
from underthesea_flow.validation.validation import TrainTestSplitValidation

from models import model_1

from preprocess import treebank, vlsp2016

if __name__ == '__main__':
    # =========================================================================#
    # Start an experiment with flow
    # =========================================================================#
    flow = Flow()
    flow.log_folder = "logs"

    # =========================================================================#
    #                               Data
    # =========================================================================#

    # for evaluation
    # file = join(dirname(__file__), "corpus", "treebank", "train.txt")
    # sentences = treebank.load_data(file)

    # for saving model
    sentences = []
    for f in ["train.txt", "dev.txt", "test.txt"]:
        file = join(dirname(__file__), "corpus", "vlsp2016", f)
        sentences += vlsp2016.load_data(file)

    flow.data(sentences=sentences)

    # =========================================================================#
    #                                Models
    # =========================================================================#
    flow.transform(model_1.transformer)
    flow.add_model(model_1.model)

    # =========================================================================#
    #                              Evaluation
    # =========================================================================#
    flow.add_score('f1_chunk')
    flow.add_score('accuracy_chunk')

    flow.set_validation(TrainTestSplitValidation(test_size=0.1))
    # =========================================================================#
    #                            Run Experiment
    # =========================================================================#

    flow.train()
    # flow.save_model("CRF", filename="postag_crf_20171005.model")
