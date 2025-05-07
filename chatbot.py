from document_qa import load_document, setup_qa_chain, ask_question_from_doc
from tools.book_appointment import start_booking_flow 

def run_chatbot(document_path):
    # Load and prepare document QA chain
    document_text = load_document(document_path)
    qa_chain = setup_qa_chain(document_text)

    print("🤖 Chatbot Ready! Type 'call me' or 'book appointment' to schedule a call, or ask a question.")
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Check for booking intent
        if "call me" in user_input.lower() or "book appointment" in user_input.lower():
            start_booking_flow()
        else:
            # Ask question from document using retriever
            try:
                answer = ask_question_from_doc(qa_chain, user_input)
                print("🤖:", answer["result"])
            except Exception as e:
                print("⚠️ Error while answering your question:", str(e))
