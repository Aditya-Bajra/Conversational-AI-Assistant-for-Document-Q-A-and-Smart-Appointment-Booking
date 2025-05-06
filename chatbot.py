from document_qa import load_document, setup_qa_chain, ask_question_from_doc
from tools.validators import is_valid_email, is_valid_phone
from tools.date_parser import parse_human_date
from storage import save_booking

def run_chatbot(document_path):
    # Load and prepare document QA chain
    document_text = load_document(document_path)
    qa_chain = setup_qa_chain(document_text)

    print("🤖 Chatbot Ready! Type 'call me' to book an appointment or ask a question.")
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Check for booking intent
        if "call me" in user_input.lower():
            while True:
                name = input("Your name: ")
                email = input("Your email: ")
                phone = input("Your phone number: ")
                appointment_text = input("When should we contact you?\n")

                if not is_valid_email(email):
                    print("❌ Invalid email format.")
                    continue

                if not is_valid_phone(phone):
                    print("❌ Invalid phone number.")
                    continue

                date = parse_human_date(appointment_text)
                if date == "Invalid date":
                    print("❌ Couldn't understand the date. Please try again.")
                    continue

                save_booking({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "date": date
                })
                print(f"✅ Appointment booked for {name} on {date}!")
                break
        else:
            # Ask question from document using retriever
            try:
                answer = ask_question_from_doc(qa_chain, user_input)
                print("🤖:", answer["result"])
            except Exception as e:
                print("⚠️ Error while answering your question:", str(e))
