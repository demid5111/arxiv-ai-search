from sentence_transformers import SentenceTransformer

class Model:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2') -> None:
        self.model = SentenceTransformer(model_name)

    def embedding(self, sentence: str):
        return self.model.encode(sentence)


