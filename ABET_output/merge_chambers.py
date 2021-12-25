#I would like to have all these outputs go to single folders per date, not separated by chamber. So...

import os
import pandas as pd 
import subprocess

finalFolder = "G:/Shared drives/Grissom Lab UMN/ABETdata/CSV/"
outputFolder = "G:/My Drive/Coding/ABET_automated_output/outputs/"

#goal is to consolidate all four items into one thing and move to a final placement...
dbList = os.listdir(outputFolder)
dateList = []
dbDict = {} 
for db in dbList:
    dirList = [a for a in os.listdir(outputFolder+db) if os.path.isdir(os.path.join(outputFolder,db,a)) is True]
    dbDict[db] = {'dates' : dirList}
    dateList = dateList + dirList

#total list of dates for the list 
dateList=list(set(dateList))

for date in dateList:
    newDateFolder = finalFolder+date
    if os.path.isdir(newDateFolder) is False:
        os.makedirs(newDateFolder)
    for db in dbList:
        if os.path.isdir(os.path.join(outputFolder,db,date)) is True:
            oldDateFolder = outputFolder+db+'/'+date
            for file in os.listdir(oldDateFolder):
                thisFile = pd.read_csv(oldDateFolder+'/'+file)
                newFN = newDateFolder + '/' + file
                if 'summary' in file:
                    #check the old one 
                    try:
                        oldSummary = pd.read_csv(newFN)
                        newDF = pd.concat([oldSummary,thisFile])
                        newDF.to_csv(newFN,index=False)
                    except:
                        thisFile.to_csv(newFN,index=False)                        
                else:
                    thisFile.to_csv(newFN,index=False)
