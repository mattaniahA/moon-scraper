import json
from datetime import datetime
from math import fabs

file_path = "eop-iau2000-1846-now.json"
with open(file_path, "r") as file:
    eop_data = json.load(file)


def find_closest_date(date_str, data):
    # Convert input date string to datetime object
    input_date = datetime.strptime(date_str, "%Y-%m-%d")
    
    closest_date = None
    min_difference = float('inf')
    closest_eop = None

    # Iterate over the records in the JSON file to find the closest date
    for entry in data['EOP']['data']['timeSeries']:
        record_date_str = f"{entry['time']['dateYear']}-{entry['time']['dateMonth']}-{entry['time']['dateDay']}"
        record_date = datetime.strptime(record_date_str, "%Y-%m-%d")
        
        # Calculate the absolute difference between the input date and the record date
        difference = fabs((input_date - record_date).days)
        
        if difference < min_difference:
            min_difference = difference
            closest_date = record_date
            closest_eop = entry

    return closest_date, closest_eop



input_date = "1998-01-19"

closest_date, closest_eop = find_closest_date(input_date, eop_data)

# Print the results
if closest_eop:
    print(f"Input Date: {input_date}")
    print(f"Closest Date: {closest_date}")
    print("Relevant EOP Data:")
    print(json.dumps(closest_eop, indent=4))
else:
    print("No data found.")
