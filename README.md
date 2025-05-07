# Conversational-AI-Assistant-for-Document-Q-A-and-Smart-Appointment-Booking

A Conversational AI Assistant designed for Document Question & Answering and Smart Appointment Booking. This project enables users to interact with documents through natural language queries and efficiently manage appointment bookings via a smart conversational interface.

## Features

- Natural language question answering over uploaded documents (txt, PDF, docx)
- Smart appointment booking through conversational interface
- Date parsing and validation for appointment scheduling
- Modular tools for booking logic and document processing
- User-friendly Streamlit-based UI for easy interaction

## Folder Structure
```
📂 Project-root/
├── requirements.txt         # Python dependencies
├── main.py                  # Entry point
├── chatbot.py               # Conversational logic
├── document_qa.py           # Document Q&A logic
├── llm_setup.py             # Language model setup
├── storage.py               # Data storage logic
├── ui_app.py                # Streamlit UI
├── data/                    # Data folder
├── documents/               # Document files
│ ├── sample_doc.txt
│ └── Careers.pdf
├── appointments.json        # Appointment data
├── tools/                   # Booking and parsing tools
│ ├── book_appointment.py    # Booking logic
│ ├── booking_trigger.py     # Booking triggers
│ ├── date_parser.py         # Date parsing and validation
│ └── validators.py          # Input validation
└── utils/ 
└── file_utils.py            # File handling utilities
```
## Installation

Make sure you have **Python 3.10** installed. Then install the required dependencies using:
```bash
pip install -r requirements.txt
```


## Running the Application

To launch the application, run:
```bash
streamlit run ui_app.py
```

## Contribution

Contributions are welcome! If you want to contribute:

- Fork the repository
- Create a new branch for your feature or bugfix
- Submit a pull request describing your changes

Please ensure your code follows the existing style.

---

If you have any questions or feedback, feel free to reach out!
