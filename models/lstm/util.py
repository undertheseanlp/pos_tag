class IndexUtil:
    @staticmethod
    def get_tokens_to_indexes(tokens_to_indexes, tokens):
        indexes = []
        for token in tokens:
            if token in tokens_to_indexes:
                index = tokens_to_indexes[token]
            else:
                index = 0
            indexes.append(index)
        return indexes