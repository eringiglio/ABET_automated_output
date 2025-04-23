"""
This routine exists as a global update admin which can pull data from the lab folders, copy it, unpack it, and route it to other saved directories on the google drive on a daily or hourly fashion.

10/20/23 - added module to copy and save databases
"""
"""
*** USER EDITED BLOCK GOES HERE: WRITE IN FULL PATHS (e.g. example)
"""

outputDir = "/mnt/share/ABETdata/ABETdb/unpacked_databases/" #raw unpacked csv files for each database go here
inputDir = "/mnt/share/ABETdata/ABETdb/db_inputs/" #ABETdb files should go into the input folder.
finalDir = "/mnt/share/ABETdata/CSV/" #this is where all of the mouse-day files go, along with a copy of the daily summary for that day
summaryDir = "/mnt/share/ABETdata/CSV/daily_summaries/" #another copy of each daily summary file goes here
baseDir = "/mnt/share/ABETdata/ABETdb/" 

outputDir = "/home/eringiglio/ABET/ABETdb/unpacked_databases/" #raw unpacked csv files for each database go here
inputDir = "/home/eringiglio/ABET/ABETdb/db_inputs/" #ABETdb files should go into the input folder.
finalDir = "/home/eringiglio/ABET/CSV/" #this is where all of the mouse-day files go, along with a copy of the daily summary for that day
summaryDir = "/home/eringiglio/ABET/CSV/daily_summaries/" #another copy of each daily summary file goes here
baseDir = "/home/eringiglio/ABET/ABETdb/" 

os.makedirs(summaryDir)

"""
***
"""
import os
import subprocess
import shutil
from ABET_output.global_csv_processing import global_datapull
from ABET_output.global_csv_processing import recent_datapull

fileName = []
for i in os.listdir(inputDir):                             #find file names in input folder
    if i.__contains__(".ABETdb"):
        fileName.append(i)

fileName.sort()

for i in fileName:                                          #convert each found file to csv files and place them in folder
    Pcommand = "/mnt/share/Resources and Protocols/Useful scripts/ABET_automated_output/mdb2.sh", inputDir + i #mdb-export-all defines where these are written
    print(Pcommand)
    subprocess.run(Pcommand)
    if 'ephys' in i.lower():
        shutil.copy(os.path.join(inputDir,i),os.path.join(baseDir,"ephys",i))
    elif 'female' in i.lower():
        shutil.copy(os.path.join(inputDir,i),os.path.join(baseDir,"females",i))
    elif 'male' in i.lower():
        shutil.copy(os.path.join(inputDir,i),os.path.join(baseDir,"males",i))

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
