from datetime import datetime
import parsedatetime

def parse_human_date(text):
    cal = parsedatetime.Calendar()
    time_struct, parse_status = cal.parse(text)
    
    if parse_status == 0:
        return "Invalid date"
    
    parsed_date = datetime(*time_struct[:6])
    return parsed_date.date().isoformat()

# Test function with various inputs
def test_date_parser():
    test_dates = [
        "next monday",
        "tomorrow",
        "in 3 days",
        "May 10",
        "next week",
        "2023-12-25"
    ]
    
    print("Date Parser Test Results:")
    print("-" * 40)
    for date_text in test_dates:
        result = parse_human_date(date_text)
        print(f"Input: '{date_text}' → Output: {result}")

    
# test_date_parser()