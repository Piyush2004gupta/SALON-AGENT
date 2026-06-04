import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
_base = os.path.dirname(os.path.abspath(__file__))
_doc_path = os.path.join(_base, "..", "documents", "salon_knowledge_base.txt")
with open(_doc_path, "r",) as file:
    text = file.read()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
documents = text_splitter.split_text(text)

if __name__ == "__main__":
    print(f"Total chunks created: {len(documents)}")
