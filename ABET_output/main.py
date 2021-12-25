"""
Contains the bones of the code I'm pulling from sql_ABET_analyzer; as run, should check "inputs" folder for .ABETdb files, process any databases there, and save files for each run schedule named by the animal ID + date into the output folder. 
"""

#actually used
import os
import subprocess
from ABET_output.global_csv_processing import global_datapull

inputDir = 'G:/My Drive/Coding/ABET_automated_output/inputs/' #ABETdb files should go into the input folder.
outputDir = 'G:/My Drive/Coding/ABET_automated_output/outputs/' #note that where the output files go to is written in the mdb-export file.  

workingDir = os.getcwd()
loop = 0
fileName = []
for i in os.listdir(inputDir):                             #find file names in input folder
    if i.__contains__(".ABETdb"):
        fileName.append(i)

for i in fileName:                                          #convert each found file to csv files and place them in folder
    Pcommand = workingDir + "/mdb-export-all.sh", inputDir + i #mdb-export-all defines where these are written 
    subprocess.run(Pcommand)

#this will create a bunch of files in the output folder. next... 
dbList = os.listdir(outputDir)
for db in dbList:
    print(db)
    global_datapull(db)

