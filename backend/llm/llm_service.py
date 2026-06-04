import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
