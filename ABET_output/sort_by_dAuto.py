"""
Forgot to sort files for each individual mouse by DAuto output, aka the automated routine that sorts out behaviors from one file to another. This routine should fix that for all individual mouse-day files that have been generated. Fastest way is just to modify and sort all those files. Let's go... 
"""
import os
import pandas as pd


bigDir = "G:/Shared drives/Grissom Lab UMN/ABETdata/CSV/" #this is where all of the mouse-day files go, along with a copy of the daily summary for that day

yearList = [x for x in os.listdir(bigDir) if len(x) == 4]
yearList.sort()
yearList.reverse()
for year in yearList:
    dayList = os.listdir(os.path.join(bigDir,year))
    dayList.sort()
    for day in dayList:
        print(day)
        mouseList = [x for x in os.listdir(os.path.join(bigDir,year,day)) if 'summary' not in x]
        mouseList.sort()
        for mouse in mouseList:
            thisFile = os.path.join(bigDir,year,day,mouse)
            thisDF = pd.read_csv(thisFile)
            thisDF = thisDF.sort_values('DAuto')
            thisDF.to_csv(thisFile)
