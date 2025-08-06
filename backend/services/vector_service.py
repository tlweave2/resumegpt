from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import FakeEmbeddings


def _get_embeddings():
    """Use OpenAI embeddings if available else fall back to fake embeddings."""
    try:
        return OpenAIEmbeddings()
    except Exception:
        return FakeEmbeddings(size=1536)


def build_faiss_index(docs, path: str = "data/vector_store/faiss_index"):
    embeddings = _get_embeddings()
    store = FAISS.from_documents(docs, embeddings)
    store.save_local(path)
    return store


def load_faiss_index(path: str = "data/vector_store/faiss_index"):
    embeddings = _get_embeddings()
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
