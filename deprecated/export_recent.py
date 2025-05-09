"""
Contains the bones of the code I'm pulling from sql_ABET_analyzer; as run, should check "inputs" folder for .ABETdb files, process any databases there, and save files for each run schedule named by the animal ID + date into the output folder.
"""

#actually used
import os
import subprocess
import pandas as pd
from ABET_output.global_csv_processing import global_datapull
from ABET_output.merge_chambers import merge_chambers
from ABET_output.check_new_databases import check_new_databases

"""
*** USER EDITED BLOCK GOES HERE: WRITE IN FULL PATHS (e.g. example)
"""

inputDir = "H:/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/db_inputs/" #ABETdb files should go into the input folder.
outputDir = "H:/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/unpacked_databases/" #note that where the output files go to is written in the mdb-export file.
finalDir = "H:/Shared drives/Grissom Lab UMN/ABETdata/CSV/" #this is where all of the mouse-day files go, along with a copy of the daily summary for that day
summaryDir = "H:/Shared drives/Grissom Lab UMN/ABETdata/CSV/daily_summaries/" #another copy of each daily summary file goes here
linInputDir = "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/db_inputs/" #ABETdb files should go into the input folder.

"""
***
"""

#first, check for any recently updated databases
dbList = check_new_databases()

workingDir = os.getcwd()

for i in dbList:                                          #convert each found file to csv files and place them in folder
    Pcommand = "wsl","./mdb2.sh", linInputDir + i #mdb-export-all defines where these are written
    subprocess.run(Pcommand)

os.listdir(inputDir)

#let's back these up here. no reason to waste perfectly good csv explosions. send those...

#this will create a bunch of files in the output folder. next, pull those csvs apart into the animal-day csvs with summaries......
for db in dbList: #for every database in our list of databases...
    print(db)
    newDBdir = outputDir + db + '/'
    if os.path.isdir(newDBdir) is False: #if there isn't already a folder for this database in the folder for backing up the database CSV intermediate files, make one
        os.makedirs(newDBdir)
    oldDBdir = outputDir+db+'/'
    for file in os.listdir(oldDBdir): #"for every csv file in the folder of interest, read it, move it over to the new directory for storing these, and write it over there so we have a record of the intermediate file"
        if '.csv' in file:
            thisFile = pd.read_csv(oldDBdir+file) #read old file
            newFN = newDBdir + file #make a new path to put a new file into
            thisFile.to_csv(newFN,index=False) #put this csv at that place
    out = global_datapull(db) #from the global_datapull: go ahead and take all those csvs and create a bunch of helpful little syncing tips

merge_chambers(outputDir,finalDir,summaryDir)
