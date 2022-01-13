"""
This routine exists as a global update admin which can pull data from the lab folders, copy it, unpack it, and route it to other saved directories on the google drive on a daily or hourly fashion.
"""

"""
*** USER EDITED BLOCK GOES HERE: WRITE IN FULL PATHS (e.g. example)
"""

inputDir = "H:/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/db_inputs/" #ABETdb files should go into the input folder.
outputDir = "H:/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/unpacked_databases/" #raw unpacked csv files for each database go here
finalDir = "H:/Shared drives/Grissom Lab UMN/ABETdata/CSV/" #this is where all of the mouse-day files go, along with a copy of the daily summary for that day
summaryDir = "H:/Shared drives/Grissom Lab UMN/ABETdata/CSV/daily_summaries/" #another copy of each daily summary file goes here

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
    Pcommand = "./mdb-export-all.sh", inputDir + i #mdb-export-all defines where these are written
    subprocess.run(Pcommand)

Pcommand
