from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from llm_setup import get_llm

def load_document(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text

def setup_qa_chain(document_text):
    # Step 1: Split
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=chunk) for chunk in splitter.split_text(document_text)]

    # Step 2: Embed
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever()

    # Step 3: Retrieval QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=get_llm(),
        retriever=retriever,
        return_source_documents=False
    )
    return qa_chain

def ask_question_from_doc(qa_chain, question):
    return qa_chain.invoke(question)
