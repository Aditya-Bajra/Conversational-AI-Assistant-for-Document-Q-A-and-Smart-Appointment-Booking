from .models import ContactInfo, AppointmentDetails
import parsedatetime
from datetime import datetime

def validate_contact(data: dict):
    try:
        ContactInfo(**data)
        return True, ""
    except Exception as e:
        return False, str(e)

def validate_appointment(data: dict):
    try:
        AppointmentDetails(**data)
        return True, ""
    except Exception as e:
        return False, str(e)

def parse_natural_date(text: str):
    cal = parsedatetime.Calendar()
    time_struct, parse_status = cal.parse(text)
    if parse_status == 0:
        return None
    parsed_date = datetime(*time_struct[:6])
    return parsed_date.date().isoformat()
