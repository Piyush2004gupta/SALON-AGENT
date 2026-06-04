import os
import sys
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
load_dotenv(dotenv_path=os.path.join(os.path.abspath(__file__), "..", ".env"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "chunking"))
from chunk_documents import documents
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectordb = FAISS.from_texts(texts=documents, embedding=embeddings)
save_path = os.path.join(os.path.dirname(__file__), "..", "vectordb", "faiss_index")
vectordb.save_local(save_path)
print(f"Vector store saved to: {save_path}")

