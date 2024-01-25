import internetarchive as ia

# get all identifiers from collection
all_items = ia.search_items('collection:navobsy')

for result in all_items:
    print(result['identifier'])



# //////////////////////////////////////

item = ia.get_item('USNOGP_01_01_000073')

for k,v in item.metadata.items():
    print(print(k,":",v))


# ia.download('nasa', verbose=True)