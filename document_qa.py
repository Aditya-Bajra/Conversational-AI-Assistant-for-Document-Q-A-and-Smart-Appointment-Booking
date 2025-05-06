from llm_setup import get_llm

def load_document(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
def ask_question_from_doc(document, question):
    llm = get_llm()
    prompt = f"""Use the following document to answer the question.

    Document:
    {document}

    Question:
    {question}
    """

    response = llm.invoke(prompt)
    return response.content