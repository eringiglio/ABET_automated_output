## ABET SQL analyzer in python 3.x

Adapted from [sql_ABET_analyzer](https://github.com/sronilsson/sql_ABET_analyzer) courtesy of sronilsson. This package intended for slightly different goals: to take a daily updated ABETdb file, automate data upload to Google Drive, and output animal-specific files organized by animal ID and date run. Should not require SQL knowledge to operate.

#### Coverts Campden Lafayette [ABETdb touchscreen databases](http://lafayetteneuroscience.com/products/abetii-touch-screen-software) to nested dicts saved as JSON or PKL.

Designed to save time by extracting raw ABET data and outputting it in forms that can be more easily manipulated by novice Python coders in a variety of formats. Aimed to be light, flexible, and easy to automate. Should come with easy-to-run daily crontab script. Work in progress.

To run, place all databases (.ABETdb files) that should be analysed in the input folder and run main.py

##### Dependencies
* The microsoftdB --> SQLite conversion requires [mdb-export-all](https://github.com/pavlov99/mdb-export-all)
  this requires mdb-tools (installable using ''Install-Module -Name mdb-tools'' in PowerShell and in everything else "apt install mdbtools" should work okay--test this later )
* statistics
* pandas
* sqlite3
* scipy
* tqdm
* csv
* shutil
* tabulate
* glob
* xlwt
