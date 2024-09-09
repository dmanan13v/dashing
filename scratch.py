# from dataclasses import fields
# from config_service.load_config import load_config
# from config_service.asset_map import AssetMap

# map_interface = AssetMap(**load_config('asset_map'))
# field_list = [{'label': getattr(map_interface, field.name).set_name, 'value': i} 
#               for i, field in enumerate(fields(map_interface))]
# print(field_list)


from data.data_sorter import DataSorter
data_interface = DataSorter()

print(data_interface.filter_by_strings(['YINN']))