import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM

# Load environment variables
load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

st.title("PDF Paper QA (RAG + Phi + LangChain)")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
query = st.text_input("Ask a question about the PDF")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(texts, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

  
  
    llm = OllamaLLM(model="phi")


    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    if query:
        result = qa_chain.invoke({"query": query})
        st.subheader("Answer:")
        st.write(result["result"])
