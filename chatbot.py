from document_qa import load_document, ask_question_from_doc
from tools.validators import is_valid_email, is_valid_phone
from tools.date_parser import parse_human_date
from storage import save_booking

def run_chatbot(document_path):
    doc = load_document(document_path)

    print("Chatbot Ready! Type 'call me' to book an appointment.")
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if "call me" in user_input.lower():
            while True:
                name = input("Your name: ")
                email = input("Your email: ")
                phone = input("Your phone number: ")
                appointment_text = input("When should we contact you?\n")

                if not is_valid_email(email):
                    print("Invalid email format.")
                    continue

                if not is_valid_phone(phone):
                    print("Invalid phone number.")
                    continue

                date = parse_human_date(appointment_text)
                if date == "Invalid date":
                    print("Couldn't understand the date.")
                    continue

                save_booking({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "date": date
                })
                print("Appointment booked!")
                break
        else:
            answer = ask_question_from_doc(doc, user_input)
            print("🤖: ", answer)