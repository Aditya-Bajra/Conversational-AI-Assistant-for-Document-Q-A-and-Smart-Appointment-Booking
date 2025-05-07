import streamlit as st
from document_qa import load_document, setup_qa_chain, ask_question_from_doc
from tools.validators import is_valid_email, is_valid_phone
from tools.date_parser import parse_human_date
from storage import save_booking

# Load document once and prepare QA chain
@st.cache_resource
def init_qa_chain():
    document_text = load_document("data/sample_doc.txt")
    return setup_qa_chain(document_text)

qa_chain = init_qa_chain()

# Initialize chat history and booking trigger
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "booking_mode" not in st.session_state:
    st.session_state.booking_mode = False

st.title("🤖 My Smart Chatbot")

# Display chat history
for speaker, msg in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {msg}")

# If booking mode is ON, show booking form
if st.session_state.booking_mode:
    st.markdown("### 📅 Book an Appointment")
    with st.form("booking_form"):
        name = st.text_input("Your Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        date_text = st.text_input("Preferred Date (e.g., 'next Monday at 3 PM')")
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Validate inputs
            if not name.strip():
                st.error("❌ Name is required.")
            elif not is_valid_email(email):
                st.error("❌ Invalid email format.")
            elif not is_valid_phone(phone):
                st.error("❌ Invalid phone number.")
            else:
                parsed_date = parse_human_date(date_text)
                if parsed_date == "Invalid date":
                    st.error("❌ Couldn't understand the date.")
                else:
                    # Save booking
                    save_booking({
                        "name": name.strip(),
                        "email": email,
                        "phone": phone,
                        "date": parsed_date
                    })
                    st.success(f"✅ Appointment booked for {name} on {parsed_date}!")
                    st.session_state.chat_history.append(("Bot", f"✅ Appointment booked for {name} on {parsed_date}!"))
                    st.session_state.booking_mode = False  # Exit booking mode

# Chat input at the bottom (only if not booking)
def handle_user_input():
    user_input = st.session_state.input.strip()

    if not user_input:
        return

    st.session_state.chat_history.append(("You", user_input))

    # Trigger booking mode
    if "call me" in user_input.lower() or "book appointment" in user_input.lower():
        st.session_state.booking_mode = True
        st.session_state.chat_history.append(("Bot", "📅 Sure! Let's book an appointment. Please fill this form."))
    else:
        # QA from document
        answer = ask_question_from_doc(qa_chain, user_input)
        bot_reply = answer["result"]
        st.session_state.chat_history.append(("Bot", bot_reply))

    # ✅ Clear input field (Streamlit will do it before re-render)
    st.session_state.input = ""


# Only show input box when not in booking mode
if not st.session_state.booking_mode:
    st.text_input("You:", key="input", on_change=handle_user_input)