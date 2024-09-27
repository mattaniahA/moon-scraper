# dl_date_helper.py

from datetime import datetime
import re

# A map to handle abbreviated month names (e.g., 'Aug.' -> 'August')
MONTH_ABBREVIATIONS = {
    'Jan.': 'January', 'Feb.': 'February', 'Mar.': 'March', 'Apr.': 'April', 'May.': 'May',
    'Jun.': 'June', 'Jul.': 'July', 'Aug.': 'August', 'Sep.': 'September', 'Oct.': 'October',
    'Nov.': 'November', 'Dec.': 'December'
} 

# Helper function to normalize abbreviated month names
def normalize_date(date_str):
    for abbr, full in MONTH_ABBREVIATIONS.items():
        date_str = date_str.replace(abbr, full)
    return date_str

# Helper function to format the date to YYYY_MM_DD
def format_date(date_str):
    # Normalize any abbreviated month names first
    date_str = normalize_date(date_str)
    
    # Handle date ranges by taking only the first date in the range
    date_str = re.split(r'[-–]', date_str)[0].strip()  # Split on dash and trim
    
    date_formats = ['%B %d, %Y', '%Y %B %d']  # Support both "June 8, 1937" and "1869 August 7"
    
    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, date_format)
            return parsed_date.strftime('%Y_%m_%d')  # Return as 'YYYY_MM_DD'
        except ValueError:
            continue

    try:
        # Try to parse just the year if no full date can be extracted (e.g., '1937')
        parsed_year = datetime.strptime(date_str, '%Y')
        return parsed_year.strftime('%Y')
    except ValueError:
        print(f"Could not parse date: {date_str}")
        return "unknown_date"

# Function to extract date from description using regex if no 'date' field is present
def extract_date_from_description(description):
    # Search for common date patterns in description, e.g., "June 8, 1937", "August 7, 1869"
    date_patterns = [
        r'(\b\w+ \d{1,2}, \d{4}\b)',    # Matches: June 8, 1937
        r'(\b\d{4} \w+ \d{1,2}\b)',     # Matches: 1869 August 7
        r'(\b\w+\. \d{1,2}, \d{4}\b)',  # Matches: Aug. 29, 1905
        r'(\b\d{4}\b)'                  # Matches: 1937 (if no day/month found)
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, description)
        if match:
            return match.group(0)
    
    return None

# Main function to handle both date from metadata and date from description
def get_formatted_date(metadata):
    date_str = metadata.get('date')
    
    if date_str:
        if date_str == "Jan 14-19, 1926":
            return format_date("1926 January 14")
        else:
            # Use the date from the 'date' field, parsing and formatting accordingly
            return format_date(date_str)
    
    # Fallback to finding the date in the description
    description = metadata.get('description', '')
    date_from_description = extract_date_from_description(description)
    
    if date_from_description:
        return format_date(date_from_description)
    
    return "unknown_date"
