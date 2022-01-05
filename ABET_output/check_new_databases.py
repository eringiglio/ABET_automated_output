"""
Should check the computer files for any recent database updates, copy the new database files over to database directories in the ABETdb Google Drive, and unpack ONLY databases which have recently been updated.

Because this file is looking at folders which are backed up to Google Drive, rather than at the shared drive we host the files on itself, we need to use rclone to check on and copy these files instead of standard Python file reading, copying, and moving protocols.
"""
#import modules
import pandas as pd
import subprocess
import numpy as np

rclone = "H:/Shared drives/Grissom Lab UMN/ABETdata/rclone-v1.57.0/rclone.exe" #should be the full path to rclone on your installation

#this should be a dictionary of folders which you want to copy from a watched PC's ABET output directory to a secondary directory (to reduce any risk of file corruption while a database may be in use). Keys should be the original ABET System Folder location; values should be the location of this secondary directory. Note that copydict frames the shared drive in terms of the name given to that drive in rclone's config; rather than G:/Shared drives/Grissom Lab UMN, we see instead "UMNdrive"
copyDict = {
    "UMNdrive:/ABETdata/ABETdb/chamber1-4/" : "UMNdrive:/ABETdata/ABETdb/ch1-4/",
    "UMNdrive:/ABETdata/ABETdb/chamber5-8/" : "UMNdrive:/ABETdata/ABETdb/ch5-8/",
    "UMNdrive:/ABETdata/ABETdb/chamber9-12/" : "UMNdrive:/ABETdata/ABETdb/ch9-12/",
    "UMNdrive:/ABETdata/ABETdb/chamber13-16/" : "UMNdrive:/ABETdata/ABETdb/ch13-16/"}

for i in copyDict:
    Pcommand = rclone + " ls " + copyDict[i]
    out = subprocess.run(Pcommand,capture_output=True)

#this results in a binary ist, but we want a list of strings...
no.
