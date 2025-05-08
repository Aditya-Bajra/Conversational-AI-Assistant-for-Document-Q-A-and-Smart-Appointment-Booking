import streamlit as st
from datetime import datetime
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools.document_qa import process_documents, create_document_tool
from tools.forms import collect_contact_info, book_appointment
from tools.validators import validate_contact, validate_appointment, parse_natural_date
from llm_setup import get_llm
from storage import save_booking

# Initialize core components
llm = get_llm()

def initialize_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "booking_state" not in st.session_state:
        st.session_state.booking_state = {
            "step": 0,  # 0: not booking, 1: collecting contact, 2: collecting appointment, 3: done
            "data": {}
        }
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

def render_sidebar():
    with st.sidebar:
        st.header("📁 Document Management")
        uploaded_files = st.file_uploader(
            "Upload documents",
            type=["pdf", "txt", "md"],
            accept_multiple_files=True
        )
        
        if uploaded_files and not st.session_state.vector_store:
            with st.spinner("Processing documents..."):
                st.session_state.vector_store = process_documents(uploaded_files)

def conversational_booking_flow(user_message):
    state = st.session_state.booking_state
    data = state["data"]

    # Step 1: Collect Name
    if "name" not in data:
        data["name"] = user_message.strip()
        if not data["name"]:
            return "What's your name?"
        state["step"] = 1
        return "What's your email address?"

    # Step 2: Collect Email
    if "email" not in data:
        data["email"] = user_message.strip()
        valid, err = validate_contact({"name": data["name"], "email": data["email"], "phone": "1234567890"})
        if not valid:
            data.pop("email", None)
            return f"Invalid email. Please enter a valid email address."
        state["step"] = 2
        return "What's your phone number?"

    # Step 3: Collect Phone
    if "phone" not in data:
        data["phone"] = user_message.strip()
        valid, err = validate_contact({"name": data["name"], "email": data["email"], "phone": data["phone"]})
        if not valid:
            data.pop("phone", None)
            return f"Invalid phone number. Please enter a valid phone number."
        state["step"] = 3
        return "What date would you like to book? (e.g., 'next Monday')"

    # Step 4: Collect Date
    if "date" not in data:
        date_val = parse_natural_date(user_message.strip())
        if not date_val:
            return "Invalid date. Please enter a date like '2024-06-10' or 'next Monday'."
        data["date"] = date_val
        state["step"] = 4
        return "What's the purpose of your appointment?"

    # Step 5: Collect Purpose
    if "purpose" not in data:
        data["purpose"] = user_message.strip()
        valid, err = validate_appointment({"date": data["date"], "purpose": data["purpose"]})
        if not valid:
            data.pop("purpose", None)
            return "Please describe the purpose of your appointment in a few words."
        state["step"] = 5
        save_booking(data)
        return (
            f"Thank you, {data['name']}!\n\n"
            f"Appointment booked for {data['date']}.\n"
            f"We'll contact you at {data['email']} / {data['phone']}."
        )

    # Booking complete
    state["step"] = 0
    state["data"] = {}
    return None

def main():
    st.title("🤖 Smart Document & Booking Assistant")
    initialize_state()
    render_sidebar()

    # Build tools
    tools = [collect_contact_info, book_appointment]
    if st.session_state.vector_store:
        tools.append(create_document_tool(st.session_state.vector_store))

    # Prompt with agent_scratchpad and chat_history
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You're an assistant handling both documents and bookings. Rules:
1. Use document_qa for document queries.
2. Use collect_contact_info when booking mentioned.
3. Use book_appointment for scheduling.
4. Current date: {time}"""),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad")
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    # Display chat messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask a question or book an appointment...")

    # Conversational booking state
    booking_state = st.session_state.booking_state

    if user_input:
        # If in booking flow, handle step by step
        if booking_state["step"] > 0:
            reply = conversational_booking_flow(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})
            if reply:
                st.session_state.messages.append({"role": "assistant", "content": reply})
            else:
                st.session_state.messages.append({"role": "assistant", "content": "Appointment booked! ✅"})
                booking_state["step"] = 0
                booking_state["data"] = {}
            st.rerun()
        else:
            # Normal agent flow
            st.session_state.messages.append({"role": "user", "content": user_input})
            response = agent_executor.invoke({
                "input": user_input,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            # Detect if booking is triggered
            if "book" in user_input.lower() or "appointment" in user_input.lower():
                booking_state["step"] = 1
                booking_state["data"] = {}
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "OK. I'll need to collect your contact information first. What's your name?"
                })
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["output"]
                })
            st.rerun()

if __name__ == "__main__":
    main()
