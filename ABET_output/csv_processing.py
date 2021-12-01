"""
Intended to pull the output of any given DB folder into a set of folders and files including: 1) a daily summary output for all mice run on a given day; 2) folders per mouse with a csv file for each mouse per day. EMG
"""
import os
import pandas as pd
import datetime.datetime as dt

dbFolder = os.curdir + '/outputs/female9-12_DB27/'

dataDF = pd.read_csv(dbFolder+'tbl_Data.csv')
scheduleDF = pd.read_csv(dbFolder+'tbl_Schedules.csv',index_col='SID')
notesDF = pd.read_csv(dbFolder+'tbl_Schedule_Notes.csv')

#okay. so these things are all given specific SIDs which have animal ids, who runs them, etc. We want to first construct a list of all of these IDs, which can be used to pull the correct data from all individuals...
#here we will want to specify
scheduleDF['date'] = [dt.datetime.strptime(i, '%m/%d/%y %H:%M:%S').date() for i in scheduleDF.SRunDate]
scheduleDF['time'] = [dt.datetime.strptime(i, '%m/%d/%y %H:%M:%S').time() for i in scheduleDF.SRunDate]

#finding all animals in the dataframe...
SIDlist = dataDF.SID.unique()

#identifying by date--optionally, shrink this down to the SIDs run on a particular day
for i in scheduleDF.date.unique():


scheduleDay = scheduleDF[scheduleDF.date == i]
thisSIDlist = thisDay.index.unique() #at which point we can define SIDlist as these numbers only. remember, for scheduleDF but NOT dataDF the scheduleID is the index ID.
outputSummary = []
outputHeaders = ['mouseID','date_run','scheduleName','numTrialsCompleted','PercentCorrect','numTrialsCorrect','numReversals']
for j in thisSIDlist: #within each day....
    thisSch = scheduleDF.loc[j]
    if thisSch.SName == 'TestLines-PAL':
        continue
    thisData = dataDF[dataDF.SID == j] #"give me all the data that is under SID value j"
    noteMatrix = notesDF[notesDF.SID==j]
    thisNotes = pd.DataFrame(data=list(noteMatrix.NValue),index=noteMatrix.NName).T
    totalNumTrials = max(thisData[thisData.DEffectText=="_Trial_Counter"])
    outputSummary.append([thisNotes['Animal ID'][0],i.strftime('%m/%d/%y'),thisSch.SName,totalNumTrials,,])


#useful bug checking scripts
for k in thisData.DEventText.unique():
    print('%s,%s' % (k, len(thisData[thisData.DEventText == k])))

j = 447
