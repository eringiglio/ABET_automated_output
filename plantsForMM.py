import os
import pandas as pd
import subprocess
import shutil

"""
goal here is to nab all the plants and send them up Madison's way...
"""

plantList = ["aloe","bamboo","cactus","daisy","elm","fern","grass","hickory","ivy","jade","oak","palm","rose","sunflower","tulip","violet","wheat","yucca"]

CSVfolder = "G:/Shared drives/Grissom Lab UMN/ABETdata/CSV/"
MMdir = "G:/Shared drives/Grissom Lab UMN/Projects/Madison_Plants_2021_16pdel_bandit_photometry/Raw data/"

for dateDir in os.listdir(CSVfolder):
    newDir = MMdir+dateDir
    if os.path.isdir(newDir) == False:
        os.makedirs(newDir)
    for file in os.listdir(CSVfolder+dateDir):
        plantFlag = 0 #bc I want to only copy the summary file for a day if there are any goddamn plants in it but not copy it a billion times, now I have a little flag to tell me whether there were plants in THIS dir
        for plant in plantList:
            if plant in file:
                newFile = newDir+"/"+file
                oldFile = CSVfolder+dateDir+"/"+file
                shutil.copy(oldFile,newFile)
                plantFlag = 1
        if plantFlag = 1:
            sumRoot = dateDir + "_summary.csv"
            oldSummary = CSVfolder+dateDir+"/"+sumRoot
            newSummary = MMdir+dateDir+"/"+sumRoot
            shutil.copy(oldFile,newFile)
            plantFlag = 0
