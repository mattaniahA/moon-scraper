import internetarchive as ia
from datetime import datetime
import re

#######################################################################################################
######################                   DATE HELPER FUNCTIONS                   ######################
#######################################################################################################
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




#######################################################################################################
######################                   API SPECIFIC FUNCTIONS                   #####################
#######################################################################################################

def filter_by_prefix(id_list, allowed_prefixes):
    filtered_ids = []
    for curr_id in id_list:
        # Check if any of the allowed prefixes match the start of the ID
        if any(curr_id.startswith(prefix) for prefix in allowed_prefixes):
            filtered_ids.append(curr_id)

    return filtered_ids

def get_items(query:str):
    all_search_items = ia.search_items(query)
    all_ids = []
    for result in all_search_items:
        all_ids.append(result['identifier'])
    return all_ids

def print_all_metadata(id: str):
    item = ia.get_item(id)
    for k,v in item.metadata.items():
        print(k,":",v)
    return

def print_lens():
    print('-----lengths-----')
    print('all',len(all_items))
    print('blueprints',len(blueprints))
    print('reflector_40',len(reflector_40))
    print('moon',len(moon))
    print('solar_eclipse',len(solar_eclipse))
    print('chart_plates',len(chart_plates))
    filtered = len(blueprints)+len(reflector_40)+len(moon)+len(solar_eclipse)+len(chart_plates)
    print('filtered',filtered)
    print()
    print()

all_items = get_items('collection:navobsy')
blueprints = filter_by_prefix(all_items, ['USNOA_010BP'])
reflector_40 = get_items('collection:navobsy AND instrument:"USNO 40-inch reflector"')
moon = get_items('collection:navobsy AND instrument:"Watts Moon Camera"')
chart_plates = get_items('collection:navobsy AND series:"03 - Chart Plates"')
solar_eclipse = get_items('collection:navobsy AND instrument:"camera" AND title:"solar eclipse"')
solar_eclipse2_plate = get_items('collection:navobsy AND -instrument:"camera" AND title:"solar eclipse" AND title:"plate"')
# print_lens()



####################  MAIN SOLAR ECLIPSE
for item_id in solar_eclipse:
    item = ia.get_item(item_id)
    metadata = item.metadata
    
    # Access specific metadata fields
    print("item_id:", item_id)
    # print("Title:", metadata.get('title'))
    print("Date:", metadata.get('date'))
    print("    ")
    print("---------------------------------------------------------------------------------")

    date_str = metadata.get('date', 'unknown date')
    formatted_date = format_date(date_str)  # Format the date to YYYY_MM_DD

    # Downloading the file
    file_name = '04_01_0000' + item_id[-2:] + '_P1.jpg'
    file = item.get_file(file_name)
    file.download(f'downloads/hi_res/0_METADATAAA/solar_eclipse/{formatted_date}-{item_id}.jpg')


####################  SECONDARY SOLAR ECLIPSE
for item_id in solar_eclipse2_plate:
    print("item_id:", item_id)
    # print_all_metadata(item_id)
    item = ia.get_item(item_id)
    metadata = item.metadata

    formatted_date = get_formatted_date(metadata)
    print("Date:", metadata.get('date'))
    print("Formatted Date:", formatted_date)
    print("Description:", metadata.get('description'))

    print("    ")
    print("---------------------------------------------------------------------------------")

    if "USNOGP" in item_id:
        file_name = '04_01_0000' + item_id[-2:] + '_P1.jpg'
    else:
        file_name = item_id.split('_')[0] + ".jpg"
        if item_id == "g086_20211021" or  item_id == "g122_20211124":
            file_name = item_id.split('_')[0] + "_rotated.jpg"

    file = item.get_file(file_name)
    file.download(f'downloads/hi_res/0_METADATAAA/solar_eclipse/{formatted_date}-{item_id}.jpg')





limited_list = ['USNOA_010BP_26IN_0196r','USNOA_010BP_26IN_0196v','USNOA_010BP_26IN_0204r','USNOA_010BP_26IN_0204v','USNOA_010BP_26IN_0205r','USNOA_010BP_26IN_0205v','USNOA_010BP_26IN_0206r','USNOA_010BP_26IN_0206v','USNOA_010BP_26IN_0207r','USNOA_010BP_26IN_0207v','USNOA_010BP_26IN_0208r','USNOA_010BP_26IN_0208v','USNOA_010BP_26IN_0209r','USNOA_010BP_26IN_0209v','USNOA_010BP_26IN_0210r','USNOA_010BP_26IN_0210v','USNOA_010BP_26IN_0211r','USNOA_010BP_26IN_0211v','USNOA_010BP_26IN_0212r','USNOA_010BP_26IN_0212v','USNOA_010BP_26IN_0213r','USNOA_010BP_26IN_0213v','USNOA_010BP_26IN_0214v','USNOA_010BP_26IN_0215r','USNOA_010BP_26IN_0215v','USNOA_010BP_26IN_0216r','USNOA_010BP_26IN_0216v','USNOA_010BP_26IN_0217r','USNOA_010BP_26IN_0217v','USNOA_010BP_26IN_0218r','USNOA_010BP_26IN_0218v','USNOA_010BP_26IN_0219v','USNOA_010BP_26IN_0220v','USNOA_010BP_26IN_0221v','USNOA_010BP_26IN_0222r','USNOA_010BP_26IN_0222v','USNOA_010BP_26IN_0223r','USNOA_010BP_26IN_0223v','USNOA_010BP_26IN_0224r','USNOA_010BP_26IN_0224v','USNOA_010BP_26IN_0225v','USNOA_010BP_26IN_0226r','USNOA_010BP_26IN_0226v','USNOA_010BP_26IN_0227r','USNOA_010BP_26IN_0227v','USNOA_010BP_26IN_0228r','USNOA_010BP_26IN_0228v','USNOA_010BP_26IN_0229v','USNOA_010BP_26IN_0230v','USNOA_010BP_26IN_0231r','USNOA_010BP_26IN_0231v','USNOA_010BP_26IN_0232r','USNOA_010BP_26IN_0232v','USNOA_010BP_26IN_0233r','USNOA_010BP_26IN_0233v','USNOA_010BP_26IN_0234r','USNOA_010BP_26IN_0234v','USNOA_010BP_26IN_0236r','USNOA_010BP_26IN_0236v','USNOA_010BP_26IN_0237r','USNOA_010BP_26IN_0237v','USNOA_010BP_26IN_0240r','USNOA_010BP_26IN_0240v','USNOA_010BP_26IN_0241r','USNOA_010BP_26IN_0241v','USNOA_010BP_26IN_0242r','USNOA_010BP_26IN_0243r','USNOA_010BP_26IN_0243v','USNOA_010BP_26IN_0245r','USNOA_010BP_26IN_0245v','USNOA_010BP_26IN_0246r','USNOA_010BP_26IN_0246v','USNOA_010BP_26IN_0247r','USNOA_010BP_26IN_0247v','USNOA_010BP_26IN_0248r','USNOA_010BP_26IN_0248v','USNOA_010BP_26IN_0249r','USNOA_010BP_26IN_0249v','USNOA_010BP_26IN_0254r','USNOA_010BP_26IN_0254v','USNOA_010BP_26IN_0255r','USNOA_010BP_26IN_0255v','USNOA_010BP_26IN_0256r','USNOA_010BP_26IN_0256v','USNOA_010BP_26IN_0257r','USNOA_010BP_26IN_0257v','USNOA_010BP_26IN_0261r','USNOA_010BP_26IN_0261v','USNOA_010BP_26IN_0262r','USNOA_010BP_26IN_0262v','USNOA_010BP_26IN_0263r','USNOA_010BP_26IN_0263v','USNOA_010BP_26IN_0264r','USNOA_010BP_26IN_0264v','USNOA_010BP_26IN_0265r','USNOA_010BP_26IN_0265v','USNOA_010BP_26IN_0266r','USNOA_010BP_26IN_0266v','USNOA_010BP_26IN_0268r','USNOA_010BP_26IN_0268v','USNOA_010BP_26IN_0269v','USNOA_010BP_26IN_0270r','USNOA_010BP_26IN_0270v','USNOA_010BP_26IN_0271r','USNOA_010BP_26IN_0271v','USNOA_010BP_26IN_0272r','USNOA_010BP_26IN_0272v','USNOA_010BP_26IN_0273r','USNOA_010BP_26IN_0273v','USNOA_010BP_26IN_0274r','USNOA_010BP_26IN_0274v','USNOA_010BP_26IN_0279r','USNOA_010BP_26IN_0279v','USNOA_010BP_26IN_0280r','USNOA_010BP_26IN_0280v','USNOA_010BP_26IN_0300r','USNOA_010BP_26IN_0300v','USNOA_010BP_26IN_0301r','USNOA_010BP_26IN_0301v','USNOA_010BP_26IN_0302r','USNOA_010BP_26IN_0302v']

# for item_id in limited_list:
#     item = ia.get_item(item_id)
#     # modified_id = item_id[: -4] + item_id[-3:]
#     print('~ id = ', item_id)
#     file_name =  item_id + '.jpg'
#     file = item.get_file(file_name)
    
#     if file.size > 0:
#         print(file)
#         file.download('downloads/hi_res/blueprints/'+file_name)
#     else:
#         print('!!!file doesnt exist!!!')


# for item_id in reflector_40:
#     item = ia.get_item(item_id)
#     ia.download(item_id, formats="JPEG", destdir='downloads/hi_res/reflector_40/', verbose=True)


# for item_id in moon:
#     item = ia.get_item(item_id)
#     ia.download(item_id, formats="JPEG", destdir='downloads/hi_res/marginal_moon/', verbose=True)

# for item_id in chart_plates:
#     ia.download(item_id, formats="JPEG", destdir='downloads/hi_res/chart_plates', verbose=True)





