#I want to look for places where files appear to have been incompletely extracted within the larger corpus of the CSV files. 

baseDir="/scratch.global/CSV/"

baseDir="/mnt/g/Shared drives/Grissom Lab UMN/ABETData/CSV/"
ls $baseDir


ls -lRh CSV |grep | awk '{print $2}'