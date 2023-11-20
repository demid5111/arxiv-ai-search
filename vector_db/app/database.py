import chromadb
import random
import hashlib


class DataBase:
    def __init__(self, settings: dict) -> None:
        chroma_client = chromadb.Client()
        self.collection = chroma_client.create_collection(**settings)

    def _generate_random_hash(self) -> None:
        return hashlib.sha256(random.getrandbits(4).to_bytes()).hexdigest()

    def add(self, documents: list[str], embeddings: list[float]) -> None:
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=documents,
            ids=[self._generate_random_hash() for _ in documents]
        )

    def query(self, query: str):
        return self.collection.query(
            query_texts=[query],
            n_results=2
        )