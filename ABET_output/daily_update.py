"""
This routine exists as a global update admin which can pull data from the lab folders, copy it, unpack it, and route it to other saved directories on the google drive on a daily or hourly fashion.
"""
"""
*** USER EDITED BLOCK GOES HERE: WRITE IN FULL PATHS (e.g. example)
"""

inputDir = "G:/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/db_inputs/" #ABETdb files should go into the input folder.
outputDir = "G:/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/unpacked_databases/" #raw unpacked csv files for each database go here
finalDir = "G:/Shared drives/Grissom Lab UMN/ABETdata/CSV/" #this is where all of the mouse-day files go, along with a copy of the daily summary for that day
summaryDir = "G:/Shared drives/Grissom Lab UMN/ABETdata/CSV/daily_summaries/" #another copy of each daily summary file goes here
linInputDir = "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/db_inputs/" #ABETdb files should go into the input folder.

"""
***
"""
import os
import subprocess
import pandas as pd
from ABET_output.global_csv_processing import global_datapull
from ABET_output.merge_chambers import merge_chambers
from ABET_output.check_new_databases import check_new_databases

workingDir = os.getcwd()

dbList = check_new_databases()
for i in dbList:                                          #convert each found file to csv files and place them in folder
    Pcommand = "wsl","./mdb2.sh", linInputDir + i #mdb-export-all defines where these are written
    subprocess.run(Pcommand)
