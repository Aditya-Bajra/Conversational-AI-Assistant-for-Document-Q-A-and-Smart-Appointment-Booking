from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from llm_setup import get_llm
from utils.file_utils import load_documents_from_folder


def setup_qa_chain(folder_path="data/documents/"):
    """
    Sets up a FAISS-based RetrievalQA chain using Gemini for answering questions
    from a given document text.
    """

    all_text = load_documents_from_folder(folder_path)
    document_text = "\n".join(all_text)
    # Step 1: Split document into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=chunk) for chunk in splitter.split_text(document_text)]

    # Step 2: Embed chunks using Gemini Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever()

    # Step 3: Create a custom prompt for QA
    prompt = PromptTemplate.from_template(
        """You are an expert assistant answering questions based on a given document.

Context:
{context}

Question:
{question}

Answer in a clear, concise and human-like manner. If the answer isn't in the document, say you do not have that information."""
    )

    # Step 4: Build the QA chain with the custom prompt
    qa_chain = RetrievalQA.from_chain_type(
        llm=get_llm(),
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False
    )

    return qa_chain


def ask_question_from_doc(qa_chain, question: str):
    """
    Invokes the QA chain with the user's question and returns the response.
    """
    return qa_chain.invoke({"query": question})
