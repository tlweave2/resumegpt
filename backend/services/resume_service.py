from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import CharacterTextSplitter


def load_resume(path: str):
    """Load a resume PDF or DOCX and split into chunks."""
    if path.endswith(".pdf"):
        pages = PyPDFLoader(path).load()
    else:
        pages = Docx2txtLoader(path).load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(pages)
