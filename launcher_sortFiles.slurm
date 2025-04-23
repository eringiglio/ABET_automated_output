#!/bin/bash -l
#SBATCH --time=24:00:00
#SBATCH --ntasks=8
#SBATCH --mem=30g
#SBATCH --tmp=30g
#SBATCH --mail-type=ALL
#SBATCH --mail-user=gigli029@umn.edu
#SBATCH --job-name=sortCSVs
#SBATCH --output=/scratch.global/gigli029/sortCSVs.o%j
#SBATCH --error=/scratch.global/gigli029/sortCSVs.e%j


#first pull the stuff that we need from the google drive...
rclone -v sync UMNdrive:/ABETdata/CSV/ /scratch.global/gigli029/CSV/

python /scratch.global/gigli029/CSV/sort_by_dAuto_msi.py

#now we pass all new data back
rclone -v copy /scratch.global/gigli029/CSV/ UMNdrive:/ABETdata/CSV/