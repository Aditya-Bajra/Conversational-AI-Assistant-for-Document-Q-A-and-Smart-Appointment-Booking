from dateparser import parse
from datetime import datetime

def parse_human_date(text):
    parsed = parse(text, settings={
        'PREFER_DATES_FROM': 'future',
        'RELATIVE_BASE' : datetime.now(),
        'STRICT_PARSING' : False
    })
    return parsed.isoformat() if parsed else "Invalid date"
