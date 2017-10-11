from underthesea_flow.model import Model
from underthesea_flow.model.crf import CRF
from underthesea_flow.transformer.tagged import TaggedTransformer

# ============================================================================ #
#                                Transformer
# ============================================================================ #
template = [
    "T[-2].lower", "T[-1].lower", "T[0].lower", "T[1].lower", "T[2].lower",
    "T[0].istitle", "T[-1].istitle", "T[1].istitle",
    # word unigram and bigram
    "T[-2]", "T[-1]", "T[0]", "T[1]", "T[2]",
    "T[-2,-1]", "T[-1,0]", "T[0,1]", "T[1,2]",
    # pos unigram and bigram
    "T[-3][1]", "T[-2][1]", "T[-1][1]",
    "T[-3,-2][1]", "T[-2,-1][1]",
]
transformer = TaggedTransformer(template)

# ============================================================================ #
#                                Model
# ============================================================================ #
crf_params = {
    'c1': 1.0,  # coefficient for L1 penalty
    'c2': 1e-3,  # coefficient for L2 penalty
    'max_iterations': 1000,  #
    # include transitions that are possible, but not observed
    'feature.possible_transitions': True
}
model = Model(CRF(params=crf_params), "CRF")
