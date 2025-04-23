"""
This routine exists as a global update admin which can pull data from the lab folders, copy it, unpack it, and route it to other saved directories on the google drive on a daily or hourly fashion.

THIS example is for use when one or more of the ABET computers is not hooked up to the Internet or the Google Drive.
"""
"""
*** USER EDITED BLOCK GOES HERE: WRITE IN FULL PATHS (e.g. example)
"""

outputDir = "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/unpacked_databases/" #raw unpacked csv files for each database go here
inputDir = "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/db_inputs/" #ABETdb files should go into the input folder.
finalDir = "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/CSV/" #this is where all of the mouse-day files go, along with a copy of the daily summary for that day
summaryDir = "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/CSV/daily_summaries/" #another copy of each daily summary file goes here
linInputDir = "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/db_inputs/" #ABETdb files should go into the input folder.

"""
***
"""
import os
import subprocess
import pandas as pd
from ABET_output.global_csv_processing import global_datapull
from ABET_output.global_csv_processing import recent_datapull
from ABET_output.check_ephys_databases import check_ephys_databases

fileList = check_ephys_databases()

fileName = []
for i in os.listdir(inputDir):                             #find file names in input folder
    if i.__contains__(".ABETdb"):
        fileName.append(i)

fileName.sort()

for i in fileName:                                          #convert each found file to csv files and place them in folder
    Pcommand = "/mnt/g/Shared drives/Grissom Lab UMN/Resources and Protocols/Useful scripts/ABET_automated_output/mdb2.sh", linInputDir + i #mdb-export-all defines where these are written
    subprocess.run(Pcommand)

#let's back these up here. no reason to waste perfectly good csv explosions. send those...
dbList = [x[0:len(x)-7] for x in fileName]
dbList.sort()

#this will create a bunch of files in the output folder. next, pull those csvs apart into the animal-day csvs with summaries......
for db in dbList: #for every database in our list of databases...
    print(db)
    oldDBdir = outputDir+db+'/'
    out = global_datapull(db,oldDBdir,finalDir) #from the global_datapull: go ahead and take all those csvs and create a bunch of helpful little syncing tips

#add the new thing: copy everything from the female photometry database to the shared drive for photometry

#Pcommand = (['/mnt/c/Users/psyc-grissomlab/Downloads/rclone/rclone.exe', '-v','copy', 'UMNdrive:/PHOTOdb/pcLinks/photoFemales/Experiment1-211019-185706/', 'UMNdrive:/PHOTOdb/rawDB/'])
 #'./copy_photodb.sh' #mdb-export-all defines where these are written
#subprocess.run(Pcommand)
