import sqlite3

def latencyCalc(currentSID, currentDB):
    loop = 0
    meanResponseLatency = meanCorrectLatency = meanIncorrectLatency = 0.00
    conn = sqlite3.connect(currentDB, isolation_level=None, timeout=10)
    c = conn.cursor()
    c.execute("PRAGMA TEMP_STORE = OFF")
    c.execute("PRAGMA SYNCHRONOUS = OFF")
    c.execute("PRAGMA JOURNAL_MODE = OFF")
    c.execute('DROP TABLE IF EXISTS ResponseLatencies')
    c.execute('DROP TABLE IF EXISTS ResponseLatencies2')
    c.execute('DROP TABLE IF EXISTS CorrectResponseLatencies')
    c.execute('DROP TABLE IF EXISTS IncorrectResponseLatencies')
    c.execute('DROP TABLE IF EXISTS RewardRetrieval')
    c.execute("CREATE TABLE ResponseLatencies2 (StimulusON integer)")
    c.execute("CREATE TABLE ResponseLatencies (StimulusON integer, StimulusOFF integer, TrialOutcome text, ResponseTime integer)")
    c.execute("CREATE TABLE CorrectResponseLatencies (CorrectResponseTimes integer)")
    c.execute("CREATE TABLE IncorrectResponseLatencies (IncorrectResponseTimes INTEGER)")
    c.execute("CREATE TABLE RewardRetrieval (HitTime integer, RetrievalTime integer, RetrievalLatency integer)")
    conn.commit()


    #CALCULATE ALL RESPONSE LATENCIES
    stimONSETtimes = c.execute("SELECT DTime FROM tbl_data WHERE (SID = ? AND DEffectText = ?) ORDER BY DTime", (currentSID, str('Display Image')))
    stimONSETtimes = stimONSETtimes.fetchall()
    c.executemany("INSERT INTO ResponseLatencies2 (StimulusON) VALUES (?)", stimONSETtimes)

    stimOFFSETtimes = c.execute("SELECT DTime, DEffectText FROM tbl_data WHERE SID = ? AND (DEffectText = ? OR DEffectText = ? OR DEffectText = ? OR DEffectText = ? OR DEffectText = ?) ORDER BY Dtime", (currentSID, str('Hit'), str('Missed Hit'), str('Mistake'), str('Correct Rejection'), str('Correction Trial Correct Rejection')))
    stimOFFSETtimes = stimOFFSETtimes.fetchall()

    if (len(stimONSETtimes)) != (len(stimOFFSETtimes)):
        maxRowID = int(len(stimONSETtimes))
        c.execute("DELETE FROM ResponseLatencies2 WHERE ROWID = ?", (maxRowID,))
        conn.commit()

    stimONSETtimes = c.execute("SELECT * FROM ResponseLatencies2")
    stimONSETtimes = stimONSETtimes.fetchall()

    if len(stimOFFSETtimes) > 0:
        for i in range(len(stimONSETtimes)):
            ONTime = (stimONSETtimes[loop])
            ONTime = float(ONTime[0])
            OFFTime, outcome = stimOFFSETtimes[loop]
            OFFTime = float(OFFTime)
            timeDiff = (OFFTime - ONTime)
            c.execute("INSERT INTO ResponseLatencies (StimulusON, StimulusOFF, TrialOutcome, ResponseTime) VALUES (?,?,?,?)",(ONTime, OFFTime, outcome, timeDiff))
            loop += 1

        c.execute("DELETE FROM ResponseLatencies WHERE TrialOutcome = ? OR TrialOutcome = ? OR TrialOutcome = ?", (str('Missed Hit'), str('Correct Rejection'), str('Correction Trial Correct Rejection')))
        c.execute('DROP TABLE IF EXISTS ResponseLatencies2')
        meanResponseLatency = c.execute("SELECT AVG(ResponseTime) FROM ResponseLatencies")
        meanResponseLatency = meanResponseLatency.fetchone()
        meanResponseLatency = str(meanResponseLatency[0])
        if meanResponseLatency == 'None':
            meanResponseLatency = 0.00
        meanResponseLatency = float(meanResponseLatency)
        conn.commit()

        # CALCULATE CORRECT RESPONSE LATENCIES
        hit = str('Hit')
        correctLatencies = c.execute("SELECT ResponseTime FROM ResponseLatencies WHERE TrialOutcome = ?", (hit,))
        correctLatencies = correctLatencies.fetchall()
        c.executemany("INSERT INTO CorrectResponseLatencies (CorrectResponseTimes) VALUES (?)", correctLatencies)
        meanCorrectLatency = c.execute("SELECT AVG(CorrectResponseTimes) FROM CorrectResponseLatencies")
        meanCorrectLatency = meanCorrectLatency.fetchone()
        meanCorrectLatency = str(meanCorrectLatency[0])
        if meanCorrectLatency == 'None':
            meanCorrectLatency = 0.00
            meanCorrectLatency = float(meanCorrectLatency)
        conn.commit()

        # CALCULATE INCORRECT RESPONSE LATENCIES
        mistake = str('Mistake')
        incorrectLatencies = c.execute("SELECT ResponseTime FROM ResponseLatencies WHERE TrialOutcome = ?", (mistake,))
        incorrectLatencies = incorrectLatencies.fetchall()
        c.executemany("INSERT INTO IncorrectResponseLatencies (IncorrectResponseTimes) VALUES (?)", incorrectLatencies)
        meanIncorrectLatency = c.execute("SELECT AVG(IncorrectResponseTimes) FROM IncorrectResponseLatencies")
        meanIncorrectLatency = meanIncorrectLatency.fetchone()
        meanIncorrectLatency = str(meanIncorrectLatency[0])
        if meanIncorrectLatency == 'None':
            meanIncorrectLatency = 0.00
            meanIncorrectLatency = float(meanIncorrectLatency)
        conn.commit()

    if len(stimOFFSETtimes) == 0:
        meanResponseLatency = meanCorrectLatency = meanIncorrectLatency = 0.00
        conn.commit()

    loop = 0

    # CALCULATE RETRIEVAL LATENCIES
    hitTimes = c.execute("SELECT DTime FROM tbl_data WHERE SID = ? AND DEffectText = ? ORDER BY Dtime", (currentSID, str('Hit')))
    hitTimes = hitTimes.fetchall()
    retrieveTimes = c.execute("SELECT DTime FROM tbl_data WHERE SID = ? AND DEffectText = ? ORDER BY Dtime", (currentSID, str('Reward Collected Start ITI')))
    retrieveTimes = retrieveTimes.fetchall()
    if (len(hitTimes)) != (len(retrieveTimes)):
        hitTimes = hitTimes[:-1]
    for i in range(len(hitTimes)):
        hitT = hitTimes[loop]
        hitT = float(hitT[0])
        retT = retrieveTimes[loop]
        retT = float(retT[0])
        timeD = (retT - hitT)
        if timeD < 30:
            c.execute("INSERT INTO RewardRetrieval (HitTime, RetrievalTime, RetrievalLatency) VALUES (?,?,?)", (hitT, retT, timeD))
        loop += 1

    meanRetrievalLatency = c.execute("SELECT AVG(RetrievalLatency) FROM RewardRetrieval")
    meanRetrievalLatency = meanRetrievalLatency.fetchone()
    meanRetrievalLatency = str(meanRetrievalLatency[0])
    if meanRetrievalLatency == 'None':
        meanRetrievalLatency = 0.00
        meanRetrievalLatency = float(meanRetrievalLatency)

    conn.commit()
    conn.close()

    return meanResponseLatency, meanCorrectLatency, meanIncorrectLatency, meanRetrievalLatency
