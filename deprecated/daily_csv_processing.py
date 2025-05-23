"""
Intended to pull the output of any given DB folder into a set of folders and files including: 1) a daily summary output for all mice run on a given day; 2) folders per mouse with a csv file for each mouse per day. This version is intended to pull only the most recent day and create its folders. EMG, 12/2021

Input arguments: default datemode is "latest", meaning this routine will only output the files for the most recent date contained in the dataset. Other modes include: 'named', in which you can input a specific date or dates as a list for outputs specific to those dates. 

Example inputs:

daily_datapull(db)
daily_datapull(db,datemode='named',daterange=[datetime.date(2021,12,1),datetime.date(2021,12,2),datetime.date(2021,12,3)])
"""
import os
import pandas as pd
import datetime as dt

def daily_datapull(db,datemode='latest',daterange=[]): 

db = 'female13-16_DB27'

    dbFolder = os.path.abspath(os.curdir + '/outputs/' + db + '/') #get the folder path for where I am right now
    dataDF = pd.read_csv(dbFolder+'/tbl_Data.csv') #note that this syntax, whether or not there's the slash, seems to be an annoying powershell thing that may need tweaking
    scheduleDF = pd.read_csv(dbFolder+'/tbl_Schedules.csv',index_col='SID')
    notesDF = pd.read_csv(dbFolder+'/tbl_Schedule_Notes.csv')
    #okay. so these things are all given specific SIDs which have animal ids, who runs them, etc. We want to first construct a list of all of these IDs, which can be used to pull the correct data from all individuals...
    #here we will want to specify
    scheduleDF['date'] = [dt.datetime.strptime(i, '%m/%d/%y %H:%M:%S').date() for i in scheduleDF.SRunDate]
    scheduleDF['time'] = [dt.datetime.strptime(i, '%m/%d/%y %H:%M:%S').time() for i in scheduleDF.SRunDate]
    #finding all animals in the dataframe...
    SIDlist = dataDF.SID.unique()
    dailyList = []
    #identifying by date--optionally, shrink this down to the SIDs run on a particular day
    if datemode = 'latest':
        dateList = scheduleDF.date.max()
    elif datemode='named':
        dateList = daterange    
    for i in dateList: 
        dateFolder = os.path.abspath(dbFolder + '/' + i.strftime('%m-%d-%y') + '/')
        if os.path.isdir(dateFolder) is False: #makes sure we have a date-specific outputs folder for individual animals' information
            os.makedirs(dateFolder)
        scheduleDay = scheduleDF[scheduleDF.date == i]
        thisSIDlist = scheduleDay.index.unique() #at which point we can define SIDlist as these numbers only. remember, for scheduleDF but NOT dataDF the scheduleID is the index ID.
        outputSummary = []
        #outputHeaders = ['mouseID','date_run','scheduleName','numTrialsCompleted','PercentCorrect','numTrialsCorrect','numReversals']
        outputHeaders = ['mouseID','date_run','start_time','chamber','scheduleName','numTrialsCompleted','maxTrialLength','timeTrialCompleted','whoRan'] #v2 will involve figuring some of this out but it would actually be quite useful to have the individual outputs per animal
        for j in thisSIDlist: #within each day....
            thisSch = scheduleDF.loc[j]
            if thisSch.SName == 'TestLines-PAL':
                continue
            thisData = dataDF[dataDF.SID == j] #"give me all the data that is under SID value j"
            noteMatrix = notesDF[notesDF.SID==j]
            thisNotes = pd.DataFrame(data=list(noteMatrix.NValue),index=noteMatrix.NName).T
            totalNumTrials = max(thisData[thisData.DEffectText=="_Trial_Counter"].DValue1)
            #make the individual CSV per animal
            thisData['scheduleID'] = thisSch.SName
            animal_outfile = dateFolder + '/' + thisNotes['Animal ID'][0] + '_'+ i.strftime('%m-%d-%y') + '.csv'
            thisData.to_csv(animal_outfile,index=False)
            for key in thisNotes.keys():
                if 'who' in key.lower():
                    whoKey = key #we don't name all the keys the same thing but some variant on 'who ran' is there, so I instruct the program to hunt through the keys for the name 'who'
            outputSummary.append([thisNotes['Animal ID'][0],i.strftime('%m/%d/%y'),thisSch.time,thisSch.SEnviro,thisSch.SName,totalNumTrials,thisNotes.Max_Schedule_Time.loc[0],max(thisData.DTime),thisNotes[whoKey].loc[0]])
        #daily summary csv
        dailyDF = pd.DataFrame(data=outputSummary,columns=outputHeaders)
        dailyFile = dateFolder + '/' + i.strftime('%m-%d-%y') + '_summary.csv'
        dailyDF.to_csv(dailyFile,index=False)
        dailyList.append(dailyFile) #just a list for recordkeeping if you want to check it
    return()

#note for self: "percent correct" only really applies to some schedules: 80/20, 90/10, 100/1, but *not* BANDIT necessarily or the very early schedules. get a list: which schedules include this information, and under what nomenclature?
#schedules with metrics for 'correct': cue no reward 90-10 spatial built in reversal...
