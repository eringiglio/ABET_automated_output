"""
Intended to pull the output of any given DB folder into a set of folders and files including: 1) a daily summary output for all mice run on a given day; 2) folders per mouse with a csv file for each mouse per day. EMG

#use: db is ABET database, to be read global_database('name of ABETdb') WITHOUT the file end tabs. so if your database file is db_28.ABETdb, the use of this routine should be something like dailyList = global_database(db_28). Optional return of dailyList will just create a list of the files that you created this round; you don't need to keep or read it, everything should be written to csv.
"""
import os
import pandas as pd
import datetime as dt
import subprocess

def global_datapull(db,oldDBdir,outputFolder):
    dataDF = pd.read_csv(oldDBdir+'/tbl_Data.csv') #note that this syntax, whether or not there's the slash, seems to be an annoying powershell thing that may need tweaking
    scheduleDF = pd.read_csv(oldDBdir+'/tbl_Schedules.csv',index_col='SID')
    notesDF = pd.read_csv(oldDBdir+'/tbl_Schedule_Notes.csv')
    #okay. so these things are all given specific SIDs which have animal ids, who runs them, etc. We want to first construct a list of all of these IDs, which can be used to pull the correct data from all individuals...
    #here we will want to specify
    scheduleDF['date'] = [dt.datetime.strptime(i, '%m/%d/%y %H:%M:%S').date() for i in scheduleDF.SRunDate]
    scheduleDF['time'] = [dt.datetime.strptime(i, '%m/%d/%y %H:%M:%S').time() for i in scheduleDF.SRunDate]
    if max(scheduleDF.date) > dt.datetime.strptime("01/01/30", '%m/%d/%y').date():
        badYear_idx = scheduleDF[scheduleDF['date'] > dt.datetime.strptime("01/01/30", '%m/%d/%y').date()].index
        newdates = [x.replace(year=2023) for x in scheduleDF.loc[badYear_idx].date]
        scheduleDF.loc[badYear_idx,'date'] = newdates
    #finding all animals in the dataframe...
    SIDlist = dataDF.SID.unique()
    dailyList = []
    #identifying by date--optionally, shrink this down to the SIDs run on a particular day
    for i in scheduleDF.date.unique():
        print(i)
        dateFolder = os.path.abspath(outputFolder + "/" +i.strftime('%Y') + '/' + i.strftime('%m-%d-%y') + '/')
        if os.path.isdir(dateFolder) is False: #makes sure we have a date-specific outputs folder for individual animals' information
            os.makedirs(dateFolder)
        scheduleDay = scheduleDF[scheduleDF.date == i]
        thisSIDlist = scheduleDay.index.unique() #at which point we can define SIDlist as these numbers only. remember, for scheduleDF but NOT dataDF the scheduleID is the index ID.
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
            if len(thisData) == 0:
                continue
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
    return(dailyList)

#note for self: "percent correct" only really applies to some schedules: 80/20, 90/10, 100/1, but *not* BANDIT necessarily or the very early schedules. get a list: which schedules include this information, and under what nomenclature?
#schedules with metrics for 'correct': cue no reward 90-10 spatial built in reversal...

def recent_datapull(db,oldDBdir,outputFolder):
    dataDF = pd.read_csv(oldDBdir+'/tbl_Data.csv') #note that this syntax, whether or not there's the slash, seems to be an annoying powershell thing that may need tweaking
    scheduleDF = pd.read_csv(oldDBdir+'/tbl_Schedules.csv',index_col='SID')
    notesDF = pd.read_csv(oldDBdir+'/tbl_Schedule_Notes.csv')
    #okay. so these things are all given specific SIDs which have animal ids, who runs them, etc. We want to first construct a list of all of these IDs, which can be used to pull the correct data from all individuals...
    #here we will want to specify
    scheduleDF['date'] = [dt.datetime.strptime(i, '%m/%d/%y %H:%M:%S').date() for i in scheduleDF.SRunDate]
    scheduleDF['time'] = [dt.datetime.strptime(i, '%m/%d/%y %H:%M:%S').time() for i in scheduleDF.SRunDate]
    #finding all animals in the dataframe...
    SIDlist = dataDF.SID.unique()
    dailyList = []
    #we want to check only the last five days of each database
    dateList = scheduleDF.date.unique()
    dateList.sort()
    theseDays = dateList[len(dateList)-3:len(dateList)] #last five days in each
    for i in theseDays:
        print(i)
        dateFolder = os.path.abspath(outputFolder + "/" +i.strftime('%Y') + '/' + i.strftime('%m-%d-%y') + '/')
        if os.path.isdir(dateFolder) is False: #makes sure we have a date-specific outputs folder for individual animals' information
            os.makedirs(dateFolder)
        scheduleDay = scheduleDF[scheduleDF.date == i]
        thisSIDlist = scheduleDay.index.unique() #at which point we can define SIDlist as these numbers only. remember, for scheduleDF but NOT dataDF the scheduleID is the index ID.
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
            for key in thisNotes.keys():
                switch = 'off' #if you don't have a "who ran" parameter, skip it andmove on--something is wrong here
                if 'who' in key.lower():
                    whoKey = key #we don't name all the keys the same thing but some variant on 'who ran' is there, so I instruct the program to hunt through the keys for the name 'who'
                    switch = "on"
                    if switch == "off":
                        continue
            try:
                totalNumTrials = max(thisData[thisData.DEffectText=="_Trial_Counter"].DValue1)
            except:
                totalNumTrials = 0
            #make the individual CSV per animal
            thisData['scheduleID'] = thisSch.SName
            animal_outfile = dateFolder + '/' + thisNotes['Animal ID'][0].lower() + '_' + str(thisData.SID.unique()[0]) + '_'+ i.strftime('%m-%d-%y') + '.csv'
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
    return(dailyList)
