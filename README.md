# A python script that allows you to save radar data you get from testing the Arduino

## Setup

### Requirements you need to run the script

- Have Python Downloaded
    - This is the first step: you must install python to make this work.
    - You can download python here: https://www.python.org/downloads/
    - When you are on the installer, make sure you check off the box at the bottom that says "Add Python 3.{version_num} to PATH". * THIS IS VERY IMPORTANT *
- Have the libraries needed to run the script
    - if you have python downloaded but not the libraries, just go to windows cmd or bash (on mac), navigate to the directory that you downloaded this project in (i.e. C:\Users\{user_name}\Downloads\save_radar_data-main) and type in pip install -r requirements.txt to install the libraries.


## After setting up

you can run the script - see below how to run it
through command prompt or whatever command line you
use

### How to run the file

usage: python testradar.py [-h] [--length LENGTH]
                    [--type {car,biker,walker}]    
                    [--delete_last]

optional arguments:
-  -h, --help  show this help message and exit
-  --length LENGTH number of data points you want to collect
-  --type {car,biker,walker} Three options:
    - car,        
    - biker
    - walker
-  --delete_last delete last testing data    stored, if there's something wrong with it.