"""
Forgot to sort files for each individual mouse by DAuto output, aka the automated routine that sorts out behaviors from one file to another. This routine should fix that for all individual mouse-day files that have been generated. Fastest way is just to modify and sort all those files. Let's go... 
"""
import os
import pandas as pd


bigDir = "/scratch.global/gigli029/CSV/" #this is where all of the mouse-day files go, along with a copy of the daily summary for that day

yearList = [x for x in os.listdir(bigDir) if len(x) == 4]
yearList.sort()
yearList.reverse()
for year in yearList:
    dayList = os.listdir(os.path.join(bigDir,year))
    dayList.sort()

year = "2022"
dayList = [x for x in os.listdir(os.path.join(bigDir,year)) if "12-" in x][11:23]

dayList = dayList + ["02-03-22", "02-08-22", "02-07-22", "01-06-22", "01-05-22", "01-13-22", "01-04-22", "01-06-22", "01-10-22", "01-14-22", "01-19-22", "01-25-22", "01-24-22", "01-11-22", "01-20-22", "01-27-22", "01-28-22", "01-31-22", "01-26-22"]

for day in dayList:
    print(day)
    mouseList = [x for x in os.listdir(os.path.join(bigDir,year,day)) if 'summary' not in x]
    mouseList.sort()
    for mouse in mouseList:
        print(mouse)
        thisFile = os.path.join(bigDir,year,day,mouse)
        thisDF = pd.read_csv(thisFile)
        thisDF = thisDF.sort_values('DAuto')
        thisDF.to_csv(thisFile)
