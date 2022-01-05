"""
Should check the computer files for any recent database updates, copy the new database files over to database directories in the ABETdb Google Drive, and unpack ONLY databases which have recently been updated.

"""
#import modules
import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta

rclone = "H:/Shared drives/Grissom Lab UMN/ABETdata/rclone-v1.57.0/rclone.exe" #should be the full path to rclone on your installation

#this should be a dictionary of folders which you want to copy from a watched PC's ABET output directory to a secondary directory (to reduce any risk of file corruption while a database may be in use). Keys should be the original ABET System Folder location; values should be the location of this secondary directory.
copyDict = {
    "H:/Other computers/chamber 1-4/ABET System Folder/" : "H:/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/ch1-4/",
    "H:/Other computers/chamber 5-8/ABET System Folder/" : "H:/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/ch5-8/",
    "H:/Other computers/chamber 9-12/ABET System Folder/" : "H:/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/ch9-12/",
    "H:/Other computers/chamber 13-16/ABET System Folder/" : "H:/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/ch13-16/"}

for i in copyDict:
    fileList = os.listdir(i)
    for j in fileList:
        if '.ABETdb' in j:
            fullPath = i+j
            stat_result = os.stat(fullPath)
            lastModified = datetime.fromtimestamp(stat_result.st_mtime)
            if lastModified + timedelta(days=5) > datetime.now():



#this results in a binary ist, but we want a list of strings...
np.unpackbits(out.stdout)

out
