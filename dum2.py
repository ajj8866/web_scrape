import os
from pathlib import Path
import pandas as pd
print(os.getcwd())


# for i in os.listdir(Path(Path.cwd(), 'Datapipe', 'raw_data', 'images')):
#     print(i)

list_of_dict = [{'a': 1, 'b':2}, {'a': 3, 'b': 4}]
# print(dict_of_list.values())
#list_of_dict_converted = {key: [i[key] for key in i.keys()] for i in list_of_dict[0]} 

list_of_dict_to_dict_of_list = {key: [k[key] for k in list_of_dict] for key in list_of_dict[0]}
print(list_of_dict_to_dict_of_list)


#######################################
dict_of_list = {'a1': [5,6,7], 'b1': [8,9,10]}
#######################################
dict_of_list_to_list_of_dict = [dict(zip(dict_of_list, val)) for val in zip(*dict_of_list.values()) ]
print(dict_of_list_to_list_of_dict)

print('#'*20)
# for i in zip(*dict_of_list.values()):
#     print(i)
# print(list(zip(*dict_of_list.values())))
print(*dict_of_list.values())
print('#'*20)