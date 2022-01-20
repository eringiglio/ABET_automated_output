"""
Should check the computer files for any recent database updates, copy the new database files over to database directories in the ABETdb Google Drive, and unpack ONLY databases which have recently been updated.

"""
#import modules
import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta
import shutil

#this should be a dictionary of folders which you want to copy from a watched PC's ABET output directory to a secondary directory (to reduce any risk of file corruption while a database may be in use). Keys should be the original ABET System Folder location; values should be the location of this secondary directory.

def check_new_databases():
    db_inPath = "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/db_inputs/"
    for db in os.listdir(db_inPath): #just remove everything in this folder to make things nice and tidy
        os.remove(os.path.join(db_inPath,db))
    copyDict = {
        "/mnt/g/Other computers/chamber 1-4/ABET System Folder/" : "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/ch1-4/",
        "/mnt/g/Other computers/chamber 5-8/ABET System Folder/" : "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/ch5-8/",
        "/mnt/g/Other computers/chamber 9-12/ABET System Folder/" : "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/ch9-12/",
        "/mnt/g/Other computers/chamber 13-16/ABET System Folder/" : "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/ch13-16/"}
    dbList = []
    for i in copyDict:
        fileList = os.listdir(i)
        for j in fileList:
            if '.ABETdb' in j and 'TEST' not in j:
                fullPath = i+j
                stat_result = os.stat(fullPath)
                lastModified = datetime.fromtimestamp(stat_result.st_mtime)
                if lastModified + timedelta(days=5) > datetime.now(): #if you have last modified the ABETdb file within 1 days...
                    print(j)
                    newPath = copyDict[i] + j
                    dbPath = db_inPath + j
                    dbList.append(j)
                    shutil.copy(fullPath,newPath) #...copy that file to the other directory where they live as backup.
                    shutil.copy(fullPath,dbPath) #and also, ideally, to a single input folder I can just pull from because c'mon.
    return(dbList)
