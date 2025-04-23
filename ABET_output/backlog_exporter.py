"""
Contains the bones of the code I'm pulling from sql_ABET_analyzer; as run, should check "inputs" folder for .ABETdb files, process any databases there, and save files for each run schedule named by the animal ID + date into the output folder.
"""

#actually used
import os
import subprocess
import pandas as pd
from ABET_output.global_csv_processing import global_datapull

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

workingDir = os.getcwd()
fileName = []
for i in os.listdir(inputDir):                             #find file names in input folder
    if i.__contains__(".ABETdb"):
        fileName.append(i)

fileName.sort()

for i in fileName:                                          #convert each found file to csv files and place them in folder
    Pcommand = "wsl","./mdb2.sh", linInputDir + i #mdb-export-all defines where these are written
    subprocess.run(Pcommand)

#let's back these up here. no reason to waste perfectly good csv explosions. send those...
dbList = [x[0:len(x)-7] for x in fileName]
dbList.sort()

revisit_list = [] 

#this will create a bunch of files in the output folder. next, pull those csvs apart into the animal-day csvs with summaries......
for db in dbList: #for every database in our list of databases...
    print(db)
    oldDBdir = outputDir+db+'/'
    try:
        out = global_datapull(db,oldDBdir,finalDir) #from the global_datapull: go ahead and take all those csvs and create a bunch of helpful little syncing tips
    except:
        print("db incomplete: %s" % db)
        revisit_list.append(db)
