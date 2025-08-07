import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Optional
import os

class VectorStore:
    def __init__(self, db_path: str):
        self.client = chromadb.PersistentClient(path=db_path)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.client.get_or_create_collection(
            name="pydantic_docs",
            embedding_function=self.embedding_function
        )

    def add_documents(self, documents: List[Dict]):
        """Add documents to the vector store."""
        texts = [doc["text"] for doc in documents]
        metadatas = [
            {
                "url": doc["url"],
                "title": doc["title"],
                "author": doc.get("author"),
                "date": doc.get("date")
            }
            for doc in documents
        ]
        ids = [doc["url"] for doc in documents]
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text: str, n_results: int = 3) -> List[Dict]:
        """Query the vector store for relevant documents."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return [
            {
                "text": doc,
                "metadata": meta
            }
            for doc, meta in zip(
                results["documents"][0],
                results["metadatas"][0]
            )
        ]