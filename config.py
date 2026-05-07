from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    QDRANT_PATH = os.getenv("QDRANT_PATH")

    COLLECTION_NAME = os.getenv("COLLECTION_NAME")

    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
    RERANK_MODEL = os.getenv("RERANK_MODEL")

    USER_AGENT = os.getenv("USER_AGENT")

    TOP_K = int(os.getenv("TOP_K"))
    FINAL_TOP_K = int(os.getenv("FINAL_TOP_K"))

    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))


settings = Settings()