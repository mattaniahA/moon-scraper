import json
from datetime import datetime, timedelta
import random
import os
import re

def convert_to_datetime(eop_entry):
    year = int(eop_entry['time']['dateYear'])
    month = int(eop_entry['time']['dateMonth'])
    day = int(eop_entry['time']['dateDay'])
    return datetime(year, month, day)

closest_4_eop = {
    "closest_4_dates": {}
}

def find_closest_4_eop_dates(dates_array, eop_data):
    time_series_data = eop_data['EOP']['data']['timeSeries']
    
    # Convert the EOP time series into a list of tuples (datetime, data)
    time_series_with_dates = [(convert_to_datetime(entry), entry) for entry in time_series_data]

    for date_str in dates_array:
        input_date = datetime.strptime(date_str, "%Y_%m_%d")

        # Find the closest 4 dates based on the input date
        sorted_time_series = sorted(time_series_with_dates, key=lambda x: abs(x[0] - input_date))
        # Get the closest 4 entries
        closest_4_entries = [entry[1] for entry in sorted_time_series[:4]]

        # Append to json
        closest_4_eop["closest_4_dates"][f"{date_str}"] = closest_4_entries
    
    return closest_4_eop

def extract_dates_from_filenames(directory):
    dates_array = []
    # Regex to extract dates in the format YYYY_MM_DD from filenames
    date_pattern = re.compile(r"(\d{4})_(\d{2})_(\d{2})")

    # Iterate over files in the directory
    for filename in os.listdir(directory):
        match = date_pattern.search(filename)
        if match:
            # Reformat date as YYYY_MM_DD
            date_str = f"{match.group(1)}_{match.group(2)}_{match.group(3)}"
            dates_array.append(date_str)

    return dates_array

if __name__ == "__main__":
    # Load the original EOP data
    with open('eop-iau2000-1846-now.json', 'r') as file:
        eop_data = json.load(file)

    image_directory = "../downloads/hi_res/0_METADATAAA/solar_eclipse" 

    # Extract dates from image filenames
    dates_array = extract_dates_from_filenames(image_directory)

    print("DATES ARRAY.LENGTH", len(dates_array))
    print("unique dates", len(set(dates_array)))

    print(dates_array)

    # Find the closest 4 EOP dates
    closest_4_eop_data = find_closest_4_eop_dates(dates_array, eop_data)

    # Save the new JSON to a file
    with open('closest_4_eop.json', 'w') as outfile:
        json.dump(closest_4_eop_data, outfile, indent=4)
