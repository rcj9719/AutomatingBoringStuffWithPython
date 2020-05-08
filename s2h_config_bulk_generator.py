'''
Author : Rhuta Joshi
---------------------------------------------------------------------------------------------------
Title            : s2h_config_bulk_generator.py
Description      : This utility is developed to generate configurations from DR, required for S2H using NiFi.
Pre-requisites   :  1. DR name,format and path should be valid and existing
                    2. Output path entered should be valid and existing
                    3. "Table/View/Collection" column in Collections tab of DR should be sorted
                    4. "Table/View/Collection" column in Attributes tab of DR should be sorted
Python Version   : 3.8
---------------------------------------------------------------------------------------------------
Date                    Change Name             User              Description
April 01, 2020          Initial Draft           rcj9719           Created initial version
April 24, 2020          Update in var names     rcj9719           Change in var names and config
---------------------------------------------------------------------------------------------------
'''

import xlrd
import os

def get_unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

dr_location = input("Enter full path of DR with filename and extension : ")

work_book_xlsx = xlrd.open_workbook(dr_location)
collections_sheet = work_book_xlsx.sheet_by_index(1)
attributes_sheet = work_book_xlsx.sheet_by_index(2)

config_system_name = collections_sheet.cell_value(3, 0).lower()
config_system_name = config_system_name.replace(" ", "-")
config_schedule_group = "DAILY-FULL-LOAD"
config_ssr_id = collections_sheet.cell_value(3, 1)
config_src_db_type = collections_sheet.cell_value(3, 8).upper()

tbl_names_list = collections_sheet.col_values(2)[3:]
tbl_names_list = [i for i in tbl_names_list if i]   #cleaning column list off blank spaces

db_name_list = collections_sheet.col_values(9)[3:]
db_name_dict = {}
for j in range(len(tbl_names_list)):
    db_name_dict[tbl_names_list[j]] = db_name_dict.get(tbl_names_list[j], []) + [db_name_list[j]]
config_src_db_name = ""
config_src_schema_name = ""
config_tbl_name_override = ""
config_vol_category = "MEDIUM"
config_src_access_type = "PUBLIC"

tbl_names_list = get_unique(tbl_names_list)

json_save = input("Enter path to save configurations : ")
if not os.path.exists(json_save):
    os.makedirs(json_save)
json_save = os.path.join(json_save, config_ssr_id + "-Config.json")
file_config = open(json_save, "w+")

json_config = "[ \n"
config_column_list = ""
itr=3
for config_tbl_name in tbl_names_list:
    for db_type in db_name_dict[config_tbl_name]:
        config_column_list = ""
        try:
            while (str(attributes_sheet.cell_value(itr, 0)).strip() == str(config_tbl_name).strip()) and \
                    (str(attributes_sheet.cell_value(itr, 18)).strip() == str(db_type).strip()):
                config_column_list += str(attributes_sheet.cell_value(itr, 1)) + ","
                itr += 1
        except IndexError:
            pass
        config_src_db_name = db_type
        config_src_schema_name = db_type
        if len(db_name_dict[config_tbl_name]) == 1:
            config_tbl_name_override = ""
        else:
            config_tbl_name_override = config_src_schema_name + "_" + config_tbl_name
        json_config += "\t{ \n" \
                    "\t\t\"id\": \"\", \n" \
                    "\t\t\"ssrId\": \"" + config_ssr_id + "\", \n" \
                    "\t\t\"systemName\": \"" + config_system_name + "\", \n" \
                    "\t\t\"scheduleGroupSchedule\": \"MON:SAT\", \n" \
                    "\t\t\"scheduleGroup\": \"" + config_schedule_group + "\", \n" \
                    "\t\t\"sourceDbType\": \"" + config_src_db_type + "\", \n" \
                    "\t\t\"sourceObjectName\": \"" + config_tbl_name + "\", \n" \
                    "\t\t\"sourceDatabaseName\": \"" + config_src_db_name + "\", \n" \
                    "\t\t\"sourceSchemaName\": \"" + config_src_schema_name + "\", \n" \
                    "\t\t\"sourceDataKey\": \"\", \n" \
                    "\t\t\"sourceChangeLogIdentifier\": \"\", \n" \
                    "\t\t\"activeFlag\": \"Y\", \n" \
                    "\t\t\"tableSchedule\": \"MON:SAT\", \n" \
                    "\t\t\"fullFilterCondition\": \"TRUE\", \n" \
                    "\t\t\"incrFilterCondition\": \"\", \n" \
                    "\t\t\"nullColList\": \"\", \n" \
                    "\t\t\"ingestionOrder\": \"\", \n" \
                    "\t\t\"runtimeColumnLinking\": \"\", \n" \
                    "\t\t\"selectColumnList\": \"" + config_column_list[:-1] + "\", \n" \
                    "\t\t\"createdDatetime\": \"\", \n" \
                    "\t\t\"createdBy\": \"\", \n" \
                    "\t\t\"effectiveStartdate\": \"\", \n" \
                    "\t\t\"effectiveEnddate\": \"\", \n" \
                    "\t\t\"ingestionType\": \"FULL\", \n" \
                    "\t\t\"closingFilterCondition\": \"\", \n" \
                    "\t\t\"sourceAccessType\": \"" + config_src_access_type + "\", \n" \
                    "\t\t\"volumeCategory\": \"" + config_vol_category + "\", \n" \
                    "\t\t\"tableNameOverride\": \"" + config_tbl_name_override + "\" \n" \
                    "\t},\n"
json_config = json_config[:-2] + "\n]"
file_config.write(json_config)
file_config.close()
print("end")