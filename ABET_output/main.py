"""
Contains the bones of the code I'm pulling from sql_ABET_analyzer; as run, should check "inputs" folder for .ABETdb files, process any databases there, and print files for each run schedule named by the animal ID + date into the output folder. 
"""

<<<<<<< HEAD
<<<<<<< HEAD
#actually used
import os
import subprocess

=======
=======
>>>>>>> parent of c489b00... adding new pipeline data
import sqlite3
import os
import time

from calc2 import calc2
from userDefinitions2 import userDefinitions2
from extractUserData2 import extractUserData2
from createSQLiteDBs import createSQLiteDBs
from summary import summaryPres
from remSess import remSess
from sortCSVfile import sortCSVfile
>>>>>>> parent of c489b00... adding new pipeline data

input1 = 0 #specifying what 
extractSet = 1
extractIDs = 1
extractDAYS = 1
extractSch = 1
extractComp = 0

workingDir = os.getcwd()
loop = 0
DBsFound = []
for i in os.listdir(os.curdir):                             #find file names
if i.__contains__(".ABETdb"):
    fileName.append(i)
for i in fileName:                                          #convert each found file to csv files and place them in folder
<<<<<<< HEAD
<<<<<<< HEAD
    Pcommand = "bash mdb-export-all.sh " + i

=======
=======
>>>>>>> parent of c489b00... adding new pipeline data
Pcommand = "bash mdb-export-all.sh " + i
p = subprocess.Popen(Pcommand, stdout = subprocess.PIPE, close_fds = True, shell = True)
stdout, stderr = p.communicate()
for i in fileName:                                          #move the files to the main folder, and convert each batch of relevant csv files a single .mdb file
folderName, fileExt = fileName[loop].split(".")
folderName = str(folderName) + str('/')
file1, file2, file3, file4 = (str(folderName) + str('tbl_Data.csv')), (str(folderName) + str('tbl_Schedules.csv')), (str(folderName) + str('tbl_Schedule_Notes.csv')), str(folderName) + str('tbl_Version.csv')
shutil.copy2(file1, 'tbl_Data.csv')
shutil.copy2(file2, 'tbl_Schedules.csv')
shutil.copy2(file3, 'tbl_Schedule_Notes.csv')
shutil.copy2(file4, 'tbl_Version.csv')
dbName, dbExt = fileName[loop].split('.')
folderRM = dbName
dbName = dbName + str('.db')
DBsFound.append(dbName)
>>>>>>> parent of c489b00... adding new pipeline data
