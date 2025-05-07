import streamlit as st
from document_qa import setup_qa_chain, ask_question_from_doc
from tools.validators import is_valid_email, is_valid_phone
from tools.date_parser import parse_human_date
from storage import save_booking
from tools.booking_trigger import check_for_booking_trigger  

# Load the document QA chain once
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = setup_qa_chain()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize booking form state
if "booking_state" not in st.session_state:
    st.session_state.booking_state = {
        "step": None,
        "name": "",
        "email": "",
        "phone": "",
        "date": ""
    }

def display_chat():
    # Just show chat history in simple text
    for entry in st.session_state.chat_history:
        role = entry["role"]
        text = entry["text"]
        st.write(f"{role.capitalize()}: {text}")

def handle_booking(user_input):
    state = st.session_state.booking_state

    # Start booking
    if state["step"] is None:
        st.session_state.chat_history.append({"role": "bot", "text": "Sure! What is your name?"})
        state["step"] = "name"
        return

    # Step 1: Name
    if state["step"] == "name":
        state["name"] = user_input
        st.session_state.chat_history.append({"role": "bot", "text": "Got it. What's your email?"})
        state["step"] = "email"
        return

    # Step 2: Email
    if state["step"] == "email":
        if not is_valid_email(user_input):
            st.session_state.chat_history.append({"role": "bot", "text": "Your email format is invalid. Please enter again."})
            return
        state["email"] = user_input
        st.session_state.chat_history.append({"role": "bot", "text": "Thanks! Your phone number?"})
        state["step"] = "phone"
        return

    # Step 3: Phone
    if state["step"] == "phone":
        if not is_valid_phone(user_input):
            st.session_state.chat_history.append({"role": "bot", "text": "Invalid phone number. Please enter again."})
            return
        state["phone"] = user_input
        st.session_state.chat_history.append({"role": "bot", "text": "When should we contact you? (e.g., next Monday)"})
        state["step"] = "date"
        return

    # Step 4: Date
    if state["step"] == "date":
        parsed_date = parse_human_date(user_input)
        if parsed_date == "Invalid date":
            st.session_state.chat_history.append({"role": "bot", "text": "Couldn't understand the date. Please try (yyyy-mm-dd) format instead."})
            return
        state["date"] = parsed_date

        # Save booking
        save_booking({
            "name": state["name"],
            "email": state["email"],
            "phone": state["phone"],
            "date": state["date"]
        })

        st.session_state.chat_history.append({"role": "bot", "text": f"✅ Appointment booked for {state['name']} on {parsed_date}!"})

        # Reset booking state
        st.session_state.booking_state = {
            "step": None,
            "name": "",
            "email": "",
            "phone": "",
            "date": ""
        }
        return

# ------------- UI starts here -------------
st.title("📚 Chat with Doc + Book Appointment")
display_chat()

# Input widget with dynamic key to avoid duplication
unique_key = f"user_input_{len(st.session_state.chat_history)}"  # Ensure key is unique

user_input = st.text_input("You:", key=unique_key)

# Handle the input if it's provided
if user_input:
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    # If booking is ongoing or user has asked to book an appointment
    if st.session_state.booking_state["step"] is not None or check_for_booking_trigger(user_input):
        handle_booking(user_input)

    # Else handle as document QA
    else:
        answer = ask_question_from_doc(st.session_state.qa_chain, user_input)
        st.session_state.chat_history.append({"role": "bot", "text": answer["result"]})

    # After processing the input, rerun the app
    st.rerun()  # Re-run the script to reset everything and update the chat history
