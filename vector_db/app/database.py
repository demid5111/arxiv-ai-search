import hashlib
import random
import secrets
from pathlib import Path
from typing import Any, Optional, Union

import chromadb


class DataBase:
    def __init__(self, settings: dict[str, Any], db_path: Optional[Union[Path, str]] = None) -> None:
        chroma_client = chromadb.PersistentClient(path=db_path)
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

    def query(self, text: str, n_results: int = 10):
        return self.collection.query(
            query_texts=[text],
            n_results=n_results
        )

    def query_embedding(self, embedding: list[str], n_results: int = 10):
        return self.collection.query(
            query_embeddings=embedding.tolist(),
            n_results=n_results
        )
