"""fuck it, just going to run some very specific things """

import os
import subprocess
import pandas as pd
from ABET_output.global_csv_processing import global_datapull
from ABET_output.global_csv_processing import recent_datapull
from ABET_output.check_ephys_databases import check_ephys_databases
import datetime as dt

#troulbeshooting
outputDir = "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/unpacked_databases/" #raw unpacked csv files for each database go here
inputDir = "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/db_inputs/" #ABETdb files should go into the input folder.
outputFolder = "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/CSV/" #this is where all of the mouse-day files go, along with a copy of the daily summary for that day
summaryDir = "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/CSV/daily_summaries/" #another copy of each daily summary file goes here
linInputDir = "/mnt/g/Shared drives/Grissom Lab UMN/ABETdata/ABETdb/db_inputs/" #ABETdb files should go into the input folder.

db = 'TEST'
oldDBdir = os.path.join(outputDir,db)

dataDF = pd.read_csv(oldDBdir+'/tbl_Data.csv') #note that this syntax, whether or not there's the slash, seems to be an annoying powershell thing that may need tweaking
scheduleDF = pd.read_csv(oldDBdir+'/tbl_Schedules.csv',index_col='SID')
notesDF = pd.read_csv(oldDBdir+'/tbl_Schedule_Notes.csv')
#okay. so these things are all given specific SIDs which have animal ids, who runs them, etc. We want to first construct a list of all of these IDs, which can be used to pull the correct data from all individuals...
#here we will want to specify
scheduleDF['date'] = [dt.datetime.strptime(i, '%m/%d/%y %H:%M:%S').date() for i in scheduleDF.SRunDate]
scheduleDF['time'] = [dt.datetime.strptime(i, '%m/%d/%y %H:%M:%S').time() for i in scheduleDF.SRunDate]
#finding all animals in the dataframe...
SIDlist = [248,249]
dailyList = []
#identifying by date--optionally, shrink this down to the SIDs run on a particular day

i = scheduleDF.date.unique()[len(scheduleDF.date.unique())-1]
dateFolder = os.path.abspath(outputFolder + "/" +i.strftime('%Y') + '/' + i.strftime('%m-%d-%y') + '/')
if os.path.isdir(dateFolder) is False: #makes sure we have a date-specific outputs folder for individual animals' information
    os.makedirs(dateFolder)
scheduleDay = scheduleDF[scheduleDF.date == i]
thisSIDlist = [248,249] #at which point we can define SIDlist as these numbers only. remember, for scheduleDF but NOT dataDF the scheduleID is the index ID.
outputSummary = []
#outputHeaders = ['mouseID','date_run','scheduleName','numTrialsCompleted','PercentCorrect','numTrialsCorrect','numReversals','maxTrialLength','timeTrialCompleted','whoRan']
outputHeaders = ['mouseID','SID','dbID','date_run','start_time','chamber','scheduleName','numTrialsCompleted','maxTrialLength','timeTrialCompleted','whoRan'] #v2 will involve figuring some of this out but it would actually be quite useful to have the individual outputs per animal
#still missing: 'PercentCorrect','numTrialsCorrect','numReversals',
for j in thisSIDlist: #within each day....
    thisSch = scheduleDF.loc[j]
    if thisSch.SName == 'TestLines-PAL':
        continue
    elif thisSch.SName == 'TestLines-Pairwise':
        continue
    thisData = dataDF[dataDF.SID == j] #"give me all the data that is under SID value j"
    noteMatrix = notesDF[notesDF.SID==j]
    thisNotes = pd.DataFrame(data=list(noteMatrix.NValue),index=noteMatrix.NName).T
    keyList = [x for x in thisNotes.keys() if 'who' in x.lower()]
    try:
        whoKey = keyList[0]
    except: 
        keyList = [x for x in thisNotes.keys() if 'user' in x.lower()]
        whoKey = keyList[0]
    try:
        totalNumTrials = max(thisData[thisData.DEffectText=="_Trial_Counter"].DValue1)
    except:
        totalNumTrials = 0
    #make the individual CSV per animal
    thisData['scheduleID'] = thisSch.SName
    animal_outfile = dateFolder + '/' + thisNotes['Animal ID'][0].lower() + '_' + str(thisData.SID.unique()[0]) + '_'+ i.strftime('%m-%d-%y') + '.csv'
    thisData = thisData.sort_values('DAuto')
    thisData.to_csv(animal_outfile,index=False)
    outputSummary.append([thisNotes['Animal ID'][0],j,db,i.strftime('%m/%d/%y'),thisSch.time,thisSch.SEnviro,thisSch.SName,totalNumTrials,thisNotes.Max_Schedule_Time.loc[0],max(thisData.DTime),thisNotes[whoKey].loc[0]])
#daily summary csv
dailyDF = pd.DataFrame(data=outputSummary,columns=outputHeaders)
dailyFile = dateFolder + '/' + i.strftime('%m-%d-%y') + '_summary.csv'
try:
    oldSummary = pd.read_csv(dailyFile)
    newDaily = pd.concat([oldSummary,dailyDF])
except:
    newDaily = dailyDF
finDaily = newDaily.drop_duplicates(keep='last',subset=['mouseID','start_time','chamber','scheduleName'])
summaryCopy = outputFolder + 'daily_summaries/' + i.strftime('%m-%d-%y') + '_summary.csv'
finDaily.to_csv(dailyFile,index=False)
finDaily.to_csv(summaryCopy,index=False)
dailyList.append(dailyFile) #just a list for recordkeeping if you want to check it
