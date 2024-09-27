import os
import shutil
import internetarchive as ia
from dl_date_helper import get_formatted_date, format_date  # Import functions from dl_date_helper.py


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

# all_items = get_items('collection:navobsy')
# blueprints = filter_by_prefix(all_items, ['USNOA_010BP'])
# reflector_40 = get_items('collection:navobsy AND instrument:"USNO 40-inch reflector"')
# moon = get_items('collection:navobsy AND instrument:"Watts Moon Camera"')
chart_plates = get_items('collection:navobsy AND series:"03 - Chart Plates"')
# solar_eclipse = get_items('collection:navobsy AND instrument:"camera" AND title:"solar eclipse"')
# solar_eclipse2_plate = get_items('collection:navobsy AND -instrument:"camera" AND title:"solar eclipse" AND title:"plate"')
# print_lens()


##############################################################
####################  MAIN SOLAR ECLIPSE  ####################
##############################################################

# for item_id in solar_eclipse:
#     item = ia.get_item(item_id)
#     metadata = item.metadata
    
#     # Access specific metadata fields
#     print("item_id:", item_id)
#     # print("Title:", metadata.get('title'))
#     print("Date:", metadata.get('date'))
#     print("    ")
#     print("---------------------------------------------------------------------------------")

#     date_str = metadata.get('date', 'unknown date')
#     formatted_date = format_date(date_str)  # Format the date to YYYY_MM_DD

#     # Downloading the file
#     file_name = '04_01_0000' + item_id[-2:] + '_P1.jpg'
#     file = item.get_file(file_name)
#     file.download(f'downloads/hi_res/0_METADATAAA/solar_eclipse/{formatted_date}-{item_id}.jpg')

# for item_id in solar_eclipse2_plate:
#     print("item_id:", item_id)
#     # print_all_metadata(item_id)
#     item = ia.get_item(item_id)
#     metadata = item.metadata

#     formatted_date = get_formatted_date(metadata)
#     print("Date:", metadata.get('date'))
#     print("Formatted Date:", formatted_date)
#     print("Description:", metadata.get('description'))

#     print("    ")
#     print("---------------------------------------------------------------------------------")

#     if "USNOGP" in item_id:
#         file_name = '04_01_0000' + item_id[-2:] + '_P1.jpg'
#     else:
#         file_name = item_id.split('_')[0] + ".jpg"
#         if item_id == "g086_20211021" or  item_id == "g122_20211124":
#             file_name = item_id.split('_')[0] + "_rotated.jpg"

#     file = item.get_file(file_name)
#     file.download(f'downloads/hi_res/0_METADATAAA/solar_eclipse/{formatted_date}-{item_id}.jpg')



#######################################################
####################  GRID PLATES  ####################
#######################################################
for item_id in chart_plates:
    print("item_id:", item_id)
    item = ia.get_item(item_id)
    metadata = item.metadata

    formatted_date = get_formatted_date(metadata)
    print("Formatted Date:", formatted_date)
    print("----------------------------------------------------")

    # Use glob_pattern to download only the file that ends with "_P1.jpg"
    ia.download(item_id, glob_pattern="*_P1.jpg", destdir='downloads/hi_res/0_METADATAAA/chart_plates', no_directory=True, verbose=True)

    # After downloading, append the formatted date to the downloaded file name
    download_dir = 'downloads/hi_res/0_METADATAAA/chart_plates'
    
    # Rename the file(s) that match the pattern
    for file_name in os.listdir(download_dir):
        if file_name.endswith("_P1.jpg"):
            file_name_parts = file_name.rsplit('.', 1)  # Split the file name and extension
            new_file_name = f"{formatted_date}-{item_id}.{file_name_parts[1]}"  # Append date before the extension
            
            # Get full paths
            old_file_path = os.path.join(download_dir, file_name)
            new_file_path = os.path.join(download_dir, new_file_name)

            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed {file_name} to {new_file_name}")



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






