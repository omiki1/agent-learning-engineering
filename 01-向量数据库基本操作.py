import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
import uuid

load_dotenv()


class LongMemory:
    def __init__(self, model_path=None, device="cuda"):
        load_dotenv()
        path = os.getenv("CHROMA_PATH", "./chroma")
        if model_path is None:
            model_name = "BAAI/bge-small-zh-v1.5"
        else:
            model_name = model_path
        self.embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model_name,
            device=device
        )
        client = chromadb.PersistentClient(path)
        self.collection = client.get_or_create_collection(
            name="long_memory",
            embedding_function=self.embedding_model,
            metadata={"hnsw:space": "cosine"}
        )

    def save(self, user_id, query):
        """保存用户记忆"""
        id = f"memory_{user_id}+{uuid.uuid4()}"
        self.collection.add(
            ids=[id],
            documents=[query],
            metadatas=[{"user_id": str(user_id)}]  # ChromaDB 要求字符串
        )

    def query(self, user_id, question, n_results=3):
        """查询用户记忆"""
        rs = self.collection.query(
            query_texts=[question],
            n_results=n_results,
            where={"user_id": str(user_id)}
        )
        return rs["documents"][0]

    def query_with_distance(self, user_id, question, n_results=3):
        """查询并返回距离（相似度）"""
        rs = self.collection.query(
            query_texts=[question],
            n_results=n_results,
            where={"user_id": str(user_id)}
        )
        return rs["documents"][0], rs["distances"][0]

    def delete_by_user(self, user_id):
        """删除指定用户的所有记忆"""
        rs = self.collection.get(where={"user_id": str(user_id)})
        if rs["ids"]:
            self.collection.delete(ids=rs["ids"])
            return len(rs["ids"])
        return 0


if __name__ == "__main__":
    memory = LongMemory()
    rs = memory.query(1, "我喜欢什么")
    print(rs)
