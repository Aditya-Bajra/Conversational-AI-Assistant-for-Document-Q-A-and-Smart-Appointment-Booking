from tools.validators import is_valid_email, is_valid_phone
from tools.date_parser import parse_human_date
from storage import save_booking

def start_booking_flow():
    booking_data = {
        "name": None,
        "email": None,
        "phone": None,
        "date": None
    }

    # Step 1: Name
    while not booking_data["name"]:
        name = input("🤖 What's your full name?\n")
        if name.strip():
            booking_data["name"] = name.strip()
        else:
            print("❌ Please enter a valid name.")

    # Step 2: Email
    while not booking_data["email"]:
        email = input("🤖 Could you provide your email address?\n")
        if is_valid_email(email):
            booking_data["email"] = email
        else:
            print("❌ Invalid email format. Please try again.")

    # Step 3: Phone
    while not booking_data["phone"]:
        phone = input("🤖 Please enter your phone number.\n")
        if is_valid_phone(phone):
            booking_data["phone"] = phone
        else:
            print("❌ Invalid phone number. Please try again.")

    # Step 4: Appointment Date
    while not booking_data["date"]:
        date_text = input("🤖 When would you like to book the appointment? (e.g., 'next Monday at 3 PM')\n")
        parsed_date = parse_human_date(date_text)
        if parsed_date == "Invalid date":
            print("❌ Couldn't understand the date. Please try again.")
        else:
            booking_data["date"] = parsed_date

    # Save and confirm booking
    save_booking(booking_data)
    print(f"✅ Appointment booked for {booking_data['name']} on {booking_data['date']}!")
    print(f"📞 We will call you at {booking_data['phone']}.")
