import internetarchive as ia

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

def get_metadata(id: str):
    item = ia.get_item(id)
    for k,v in item.metadata.items():
        print(k,":",v)
    return item.metadata.items()


all_items = get_items('collection:navobsy')
blueprints = filter_by_prefix(all_items, ['USNOA_010BP'])
reflector_40 = get_items('collection:navobsy AND instrument:"USNO 40-inch reflector"')
moon = get_items('collection:navobsy AND instrument:"Watts Moon Camera"')
solar_eclipse = get_items('collection:navobsy AND instrument:"-foot camera" AND title:"solar eclipse"')
chart_plates = get_items('collection:navobsy AND series:"03 - Chart Plates"')

# print('-----lengths-----')
# print('all',len(all_items))
# print('blueprints',len(blueprints))
# print('reflector_40',len(reflector_40))
# print('moon',len(moon))
# print('solar_eclipse',len(solar_eclipse))
# print('chart_plates',len(chart_plates))
# filtered = len(blueprints)+len(reflector_40)+len(moon)+len(solar_eclipse)+len(chart_plates)
# print('filtered',filtered)
# print()
# print()



for item_id in chart_plates:
    # item = get_metadata(item_id)
    ia.download(item_id, formats="JPEG", destdir='downloads/chart_plates', verbose=True)
    
# item = get_metadata('USNOA_010BP_40IN_0123')
