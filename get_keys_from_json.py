'''
Author : Rhuta Joshi
------------------------------------------------------------------------------------------------------------------------
Title            : get_keys_from_json.py
Description      : This utility is developed to fetch keys and values from multilevel JSON
Pre-requisites   :  1. Input JSON should be valid and stored in a file
                    2. JSON file path should be valid and existing
Python Version   : 3.8
------------------------------------------------------------------------------------------------------------------------
Date                    Change Name             User              Description
April 17, 2020          Initial Draft           rcj9719           Created initial version
------------------------------------------------------------------------------------------------------------------------
'''

import json

## Sample json:
data_json = {
    'k1':'v1',
    'k2':{
        'k2a':'v2a',
        'k2b':{
            'k2ba':'v2aa',
            'k2bb':'v2bb'
        },
        'k2c':'v2c'
    },
    'k3':'v3'
}
key_list = []
key_hive_list = []
val_list = []


def get_key(key_str, json_data):
    if isinstance(json_data, dict):
        for item in json_data:
            key_str_new = key_str + '.'+item
            get_key(key_str_new,json_data[item])
    else:
        key_list.append(key_str)
        val_list.append(json_data)


if __name__ == '__main__':

    data_file_name = '<JSON file path>'
    data_file = open(data_file_name)
    data_json = json.load(data_file)
    for item in data_json:
        key_str = item
        if isinstance(data_json[item],dict):
            get_key(key_str,data_json[item])
        else:
            key_list.append(key_str)
            val_list.append(data_json[item])

    key_val_dict = {}
    for i in range(len(key_list)):
        key_val_dict[key_list[i]] = val_list[i]
    print(key_list)
    print(val_list)
    print(key_val_dict)
