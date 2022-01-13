import os
import pandas as pd
import subprocess
import shutil

"""
this script to remove all folders in madison's raw data folder if they have a
"""

plantList = ["aloe","bamboo","cactus","daisy","elm","fern","grass","hickory","ivy","jade","oak","palm","rose","sunflower","tulip","violet","wheat","yucca"]

CSVfolder = "G:/Shared drives/Grissom Lab UMN/ABETdata/CSV/"
MMdir = "G:/Shared drives/Grissom Lab UMN/Projects/Madison_Plants_2021_16pdel_bandit_photometry/Raw data/"

for i in os.listdir(MMdir):
    newDir = os.path.join(MMdir,i)
    output = os.listdir(newDir)
