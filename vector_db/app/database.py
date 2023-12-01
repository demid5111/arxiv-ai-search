import hashlib
import random
import secrets

import chromadb


class DataBase:
    def __init__(self, settings: dict) -> None:
        chroma_client = chromadb.PersistentClient(path='/home/user/projects/arxiv-ai-search/chroma')
        self.collection = chroma_client.get_or_create_collection(**settings)

    def _generate_random_hash(self) -> None:
        return hashlib.sha256(random.getrandbits(8).to_bytes()).hexdigest()

    def add(self, documents: list[str], embeddings: list[float]) -> None:
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=documents,
            ids=[secrets.token_hex(nbytes=16) for _ in range(len(documents))]
            # ids=[str(index) for index in range(len(documents))]
        )

    def query(self, query: str):
        return self.collection.query(
            query_texts=[query],
            n_results=5
        )