import torch

from sentence_transformers import SentenceTransformer


def get_device():
    """
    Get the current torch device.

    :return: The current torch device.
    """
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    return device


class Model:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2') -> None:
        self.model = SentenceTransformer(model_name, device=get_device())

    def embedding(self, sentence: str):
        return self.model.encode(sentence)


