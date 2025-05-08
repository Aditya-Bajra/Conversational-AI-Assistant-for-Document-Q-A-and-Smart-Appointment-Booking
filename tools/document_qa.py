from langchain_core.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import tempfile
import os

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def create_document_tool(vector_store):
    return create_retriever_tool(
        vector_store.as_retriever(),
        "document_qa",
        "Use this tool to answer questions from uploaded documents in a clear readable way."
    )

def process_documents(uploaded_files):
    embeddings = get_embeddings()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    all_text = []
    for file in uploaded_files:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file.getvalue())
            temp_path = temp_file.name
        
        # Load using temporary path
        if file.name.endswith(".pdf"):
            from langchain_community.document_loaders import PyPDFLoader
            loader = PyPDFLoader(temp_path)
        else:
            from langchain_community.document_loaders import TextLoader
            loader = TextLoader(temp_path)
        
        docs = loader.load()
        all_text.extend([doc.page_content for doc in docs])
        
        # Clean up temporary file
        os.unlink(temp_path)
    
    chunks = text_splitter.create_documents(all_text)
    return FAISS.from_documents(chunks, embeddings)
