"""
Contains the bones of the code I'm pulling from sql_ABET_analyzer; as run, should check "inputs" folder for .ABETdb files, process any databases there, and print files for each run schedule named by the animal ID + date into the output folder.
"""

#actually used
import os
import subprocess


#outputDir = '/outputs/' #outputs should be assigned to the output folder within the directory, but that's done in mdb. 
inputDir = '/mnt/g/My Drive/Coding/ABET_automated_output/inputs/' #ABETdb files should go into the input folder.

workingDir = os.getcwd()
loop = 0
fileName = []
for i in os.listdir(inputDir):                             #find file names in input folder
    if i.__contains__(".ABETdb"):
        fileName.append(i)

for i in fileName:                                          #convert each found file to csv files and place them in folder
    Pcommand = workingDir + "/mdb-export-all.sh", inputDir + i
    subprocess.run(Pcommand)
