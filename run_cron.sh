#!/bin/bash
#Startup script designed to set up cron in the background on any windows machine with which it has been installed. You can find helpful instructions for filepaths at: 
#https://julienharbulot.com/cron-windows.html
{
    echo "$(date)"
    eval $(ssh-agent -s)
    sudo /etc/init.d/cron start
} > /home/grissomlab/startup-scripts/last_startup.log 2>&1