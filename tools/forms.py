from langchain_core.tools import tool
from .validators import parse_natural_date

@tool
def collect_contact_info(query: str) -> dict:
    """Initiate contact information collection process."""
    return {"status": "contact_collection_started"}

@tool
def book_appointment(natural_date: str) -> str:
    """Convert natural language date to YYYY-MM-DD format."""
    parsed_date = parse_natural_date(natural_date)
    return parsed_date if parsed_date else "Invalid date format"
