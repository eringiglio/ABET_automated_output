Contains notes, planned pipeline, etc.

<<<<<<< HEAD
<<<<<<< HEAD
pipeline for analysis: 2 versions (one for exporting a day's worth of csvs, one for all csvs in a file.)
for each day, should export:
1) daily report csv to go into a "report" folder with commonly used metrics per animal
2) each animal should have its own folder. per day, script should export a csv with all data specific to that animal for that day into the animal's folder. name to follow ANIMALNAME_DD-MM-YY_HH-MM-SS format, with HH-MM-SS being the time at which the schedule started. animal folders should go into larger organizing folders specifying project (i.e. artists, plants, harrypotters).
=======
pipeline for analysis: 
>>>>>>> parent of c489b00... adding new pipeline data

take db file

<<<<<<< HEAD
find all db files
take db file. export all .csv files.
for each db:
sort outputs by day run
within each day:
sort outputs by individual animal
increment each to an individual csv
for daily-report spreadsheet:
  animal name
  schedule name
  calculate overall metrics:
    # trials
    percent accuracy
    # reversals


  Dependencies:
  mdb-export-all.sh, see mdb requirements in sqlABETanalyzer
  Python
    pandas
    datetime
  
=======
extract pieces day by day
>>>>>>> parent of c489b00... adding new pipeline data
=======
pipeline for analysis: 

take db file

extract pieces day by day
>>>>>>> parent of c489b00... adding new pipeline data
