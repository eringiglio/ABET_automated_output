"""
Contains the bones of the code I'm pulling from sql_ABET_analyzer; as run, should check "inputs" folder for .ABETdb files, process any databases there, and print files for each run schedule named by the animal ID + date into the output folder. 
"""

#actually used
import os
import subprocess


outputDir = os.curdir + '/outputs/' #outputs should be assigned to the output folder within the directory. 
inputDir = os.curdir +  '/inputs/' #ABETdb files should go into the input folder. 

workingDir = os.getcwd()
loop = 0
fileName = []
for i in os.listdir(inputDir):                             #find file names in input folder 
    if i.__contains__(".ABETdb"):
        fileName.append(i)
for i in fileName:                                          #convert each found file to csv files and place them in folder
    Pcommand = "bash mdb-export-all.sh " + i

