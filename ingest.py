from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

DATA_DIR = "data"

def load_documents():
    docs = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(DATA_DIR, file))
            docs.extend(loader.load())
    return docs

def chunk_and_index(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")

if __name__ == "__main__":
    print("📄 Loading documents...")
    all_docs = load_documents()

    print("✂️ Chunking and indexing...")
    chunk_and_index(all_docs)
    print("✅ Vector store saved to 'faiss_index'")