from qdrant_client import QdrantClient


client = QdrantClient(path="./qdrant_data")


def get_qdrant_client():
    return client