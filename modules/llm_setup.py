import os
from langchain_groq import ChatGroq

def setup_llm():
    llm = ChatGroq(
        model="llama3-70b-8192",
        temperature=0,
        max_tokens=None,
        timeout=None,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    return llm
