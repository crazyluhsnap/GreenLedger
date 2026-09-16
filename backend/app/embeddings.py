from chromadb.utils import embedding_functions


_embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def get_embedding_function():
    return _embedding_function