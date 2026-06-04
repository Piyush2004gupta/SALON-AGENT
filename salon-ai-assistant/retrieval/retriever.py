import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "..", ".env"))
db_path = os.path.join(BASE_DIR, "..", "vectordb", "faiss_index")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)

def retrieve(query: str, k: int = 5) -> list:
    
    return db.similarity_search(query, k=k)
