'''
Author : Rhuta Joshi
---------------------------------------------------------------------------------------------------
Title            : S2HConfigurationBulkGenerator.py
Description      : This utility is developed to generate configurations from DR, required for S2H using NiFi.
Pre-requisites   :  1. DR name,format and path should be valid and existing
                    2. Output path entered should be valid and existing
                    3. "Table/View/Collection" column in Collections tab of DR should be sorted
                    4. "Column Name" column in Attributes tab of DR should be sorted
Python Version   : 3.8
---------------------------------------------------------------------------------------------------
Date                    Change Name             User              Description
April 01, 2020          Initial Draft           rcj9719           Created initial version
---------------------------------------------------------------------------------------------------
'''

import xlrd
import os

mDRLocation = input("Enter full path of DR with filename and extension : ")

mWorkBook = xlrd.open_workbook(mDRLocation)
mCollectionsSheet = mWorkBook.sheet_by_index(1)
mAttributesSheet = mWorkBook.sheet_by_index(2)

mSystemName = mCollectionsSheet.cell_value(3,0).lower()
# print("mSystemName : "+mSystemName)
mSystemName = mSystemName.replace(" ", "-")
# print("mSystemNameNew : "+mSystemName)
mScheduleGroup = mSystemName.upper()+"-DAILY-FULL-LOAD"
# print("mScheduleGroup : "+mScheduleGroup)
mSsrId = mCollectionsSheet.cell_value(3,1)
# print("mSsrId : "+mSsrId)
mSourceDbType = mCollectionsSheet.cell_value(3,8).upper()
# print("mSourceDbType : "+mSourceDbType)

tableNamesList = mCollectionsSheet.col_values(2)[3:]
tableNamesList = [i for i in tableNamesList if i]   #cleaning column list off blank spaces
# temp = []
# for i in tableNamesList:
#     if i:
#         temp.append(i)
# tableNamesList = temp
dbNameList = mCollectionsSheet.col_values(9)[3:]
dbNameDict = {}
for j in range(len(tableNamesList)):
    dbNameDict[tableNamesList[j]] = dbNameList[j]
print(len(dbNameDict))
print(dbNameDict)
mSourceDatabaseName = ""
mSourceSchemaName = ""
mVolumeCategory = "MEDIUM"
mSourceAccessType = "PUBLIC"

print("TableNames: " + str(tableNamesList))

jsonsave = input("Enter path to save configurations : ")
jsonsave = os.path.join(jsonsave,mSsrId + "-Config.json")
fConfig = open(jsonsave, "w+")

mJson = "[ \n"
mSelectColumnList = ""
itr=3
for tableName in tableNamesList:
    mSelectColumnList = ""
    try:
        print(mAttributesSheet.cell_value(itr, 0) + " = " + tableName)
        while str(mAttributesSheet.cell_value(itr, 0)) == str(tableName):
            mSelectColumnList += str(mAttributesSheet.cell_value(itr, 1)) + ","
            itr += 1
    except IndexError:
        pass
    print(mSelectColumnList)
    mSourceDatabaseName = dbNameDict[tableName]
    mSourceSchemaName = dbNameDict[tableName]
    mJson += "\t{ \n" \
                "\t\t\"ssrId\": \""+ mSsrId +"\", \n" \
                "\t\t\"systemName\": \""+ mSystemName +"\", \n" \
                "\t\t\"scheduleGroupSchedule\": \"MON:SAT\", \n" \
                "\t\t\"scheduleGroup\": \"" + mScheduleGroup +"\", \n" \
                "\t\t\"sourceDbType\": \"" + mSourceDbType +"\", \n" \
                "\t\t\"sourceObjectName\": \"" + tableName +"\", \n" \
                "\t\t\"sourceConnectionName\": \"\", \n" \
                "\t\t\"sourceDatabaseName\": \"" + mSourceDatabaseName + "\", \n" \
                "\t\t\"sourceSchemaName\": \"" + mSourceSchemaName +"\", \n" \
                "\t\t\"sourceDataKey\": \"\", \n" \
                "\t\t\"sourceChangeLogIdentifier\": \"\", \n" \
                "\t\t\"activeFlag\": \"Y\", \n" \
                "\t\t\"fullFilterCondition\": \"TRUE\", \n" \
                "\t\t\"incrFilterCondition\": \"\", \n" \
                "\t\t\"nullColList\": \"\", \n" \
                "\t\t\"ingestionOrder\": \"\", \n" \
                "\t\t\"selectColumnList\": \"" + mSelectColumnList[:-1] + "\", \n" \
                "\t\t\"ingestionType\": \"FULL\", \n" \
                "\t\t\"sourceAccessType\": \"" + mSourceAccessType + "\", \n" \
                "\t\t\"volumeCategory\": \"" + mVolumeCategory + "\", \n" \
                "\t\t\"tableSchedule\": \"MON:SAT\" \n" \
                "\t},\n"
mJson = mJson[:-2]+"\n]"
fConfig.write(mJson)
fConfig.close()
print("end")