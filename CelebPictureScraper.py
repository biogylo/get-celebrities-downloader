# -*- coding: utf-8 -*-
"""
@title: CelebPictureScraper
@description: Downloads a ton of celebrity pictures from celebnames.com
@date:  Thu Jun 18 14:18:58 2020

@author: Juan Francisco Navarro
@email: navarro.juan@uabc.edu.mx

"""
import os.path

import numpy as np
import pandas as pd

import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from BasicFunctions import display_time
from ArtistScraper import get_artist_links
import wget

import re
import time
import sys



## regex getters
name_getter = re.compile("(.+) -")
pic_link_getter = re.compile('(https://www.famousbirthdays.com/(?:faces|headshots)/.{1,64}\.jpg)')
pic_filename_getter = re.compile('[^/]*\.jpg')

def get_name(driver):
    name = None
    while name == None:
        name = name_getter.match(driver.title)
    return name.group(1)

def get_all_download_links(driver):
    '''Visits a page and retrieves all download links using regex'''

    matches = pic_link_getter.findall(driver.page_source)
    download_links = list(dict.fromkeys(matches))
    return download_links # "set" turns it into a set with unique elements

def picture_dataframe(dictionary,picture_links):
    if dictionary["name"] in celebrity_picture_data.name.values or DEFAULT_PICTURE in picture_links:
        
        return False
    new_data = []
    for URL in picture_links:
        new_data.append({"name":dictionary["name"],"picture_link":URL,"picture_filename":pic_filename_getter.search(URL).group(),"downloaded":False})
    return pd.DataFrame(new_data)

TIME_BEGIN = time.perf_counter() 



DEFAULT_PICTURE = "https://www.famousbirthdays.com/faces/large-default.jpg"

PICS_DOWNLOADED = 0
PICTURE_LOCATION = "raw_pictures/"


PRE_DATA_FILENAME = "celebrity_pre_data.csv"

DATA_FILENAME = "celebrity_data.csv"
DATA_FIELDS = ["url","name", "occupation", "birth_month", "birth_day", "birth_year", "birth_city","birth_country", "age", "birth_sign"]

PICTURE_DATA_FILENAME = "celebrity_picture_data.csv"
PICTURE_DATA_FIELDS = ["name","picture_link","picture_filename","downloaded"]


## Check if celebrity data file exists, if not, create it
if os.path.exists(DATA_FILENAME):
    celebrity_data = pd.read_csv(DATA_FILENAME)
    CELEBRITY_LENGTH = len(celebrity_data.index)
    print("Loaded {0} artists from the ArtistScraper in {1}\n".format(CELEBRITY_LENGTH,display_time(time.perf_counter() - TIME_BEGIN)))
else:
    celebrity_data = pd.DataFrame(columns=DATA_FIELDS)
    celebrity_data.to_csv(DATA_FILENAME,index=False, encoding="utf-8")
    
celebrity_data = celebrity_data.append(get_artist_links()).drop_duplicates("name") # GET ARTISTS
CELEBRITY_LENGTH = len(celebrity_data.index)
print("Found {0} artists from the ArtistScraper in {1}\n".format(CELEBRITY_LENGTH,display_time(time.perf_counter() - TIME_BEGIN)))
celebrity_data.to_csv(DATA_FILENAME,index=False, encoding="utf-8")

input("INFO: Enter to LinkGetter")

## Check if celebirty picture data file exists, if not, create it
if os.path.exists(PICTURE_DATA_FILENAME):
    celebrity_picture_data = pd.read_csv(PICTURE_DATA_FILENAME)
    CELEBRITY_PICTURE_LENGTH = len(celebrity_picture_data.index)
    print("Loaded {0} picture links from the LinkGetter in {1}\n".format(CELEBRITY_PICTURE_LENGTH,display_time(time.perf_counter() - TIME_BEGIN)))
else:
    celebrity_picture_data = pd.DataFrame(columns=PICTURE_DATA_FIELDS)
    celebrity_picture_data.to_csv(PICTURE_DATA_FILENAME,index=False, encoding="utf-8")

#For the ETA timer
ELAPSED = 0
ETA = 999999
START_TIME = time.perf_counter() 
TOTAL_TIME = ETA
PICS_FOUND = 0
PICS_DOWNLOADED = 0

## Get picture links to celebrity_picture_dataframe from artist urls in celebrity_dataframe
driver = webdriver.Chrome("chromedriver.exe") ## start chrome
driver.get("https://www.famousbirthdays.com/")
driver.implicitly_wait(5)
## Download only those artists not on the picture link list
to_do = [(name not in celebrity_picture_data.name.values) for name in celebrity_data.name.values]
TO_DO_LENGTH = len(celebrity_data[to_do].index)
print(TO_DO_LENGTH)



for INDEX, DICT in celebrity_data[to_do].iterrows():
    try:
        driver.get(DICT["url"]) #loads next celebrity
    except:
        print("Failed at " + DICT["url"])
        driver.get(DICT["url"]) #loads next celebrity
        
        
    picture_links = get_all_download_links(driver)
    new_data = picture_dataframe(DICT,picture_links)
    
    if isinstance(new_data,pd.DataFrame) and len(picture_links) >= 1:
        celebrity_picture_data = celebrity_picture_data.append(new_data,ignore_index=True).drop_duplicates("picture_filename")
        celebrity_picture_data.to_csv(PICTURE_DATA_FILENAME,index=False, encoding="utf-8")
        
        PICS_FOUND += len(picture_links)
        ELAPSED = time.perf_counter() - START_TIME
        TOTAL_TIME = TO_DO_LENGTH*ELAPSED/(INDEX+1)
        ETA = TOTAL_TIME-ELAPSED
        
        print("LinkGetter: Artist {0} of {1},\t {2} %. \n\tName = {3}\n\tPics found = {4}.\n\tElapsed = {5}.\n\tTotal time = {6}.\n\tETA = {7}".format(INDEX,TO_DO_LENGTH,100*INDEX/TO_DO_LENGTH,DICT["name"],PICS_FOUND,display_time(ELAPSED),display_time(TOTAL_TIME),display_time(ETA)))
    else:
        celebrity_data = celebrity_data[celebrity_data.name != DICT["name"]]
        print("LinkGetter: Artist {0} of {1} INVALID PICTURE, removing from dataframe,\t {2} %. \n\tName = {3}\n\tPics found = {4}.\n\tElapsed = {5}.\n\tTotal time = {6}.\n\tETA = {7}".format(INDEX,TO_DO_LENGTH,100*INDEX/TO_DO_LENGTH,DICT["name"],PICS_FOUND,display_time(ELAPSED),display_time(TOTAL_TIME),display_time(ETA)))

driver.close()

celebrity_pictures_to_download = celebrity_picture_data[celebrity_picture_data.downloaded==False] 
TOTAL_PICS = len(celebrity_pictures_to_download.index)
print("Found {0} picture download pending links from the LinkGetter in {1}\n".format(TOTAL_PICS,display_time(ELAPSED)))

input("INFO: Enter to Downloader")

celebrity_data.to_csv(DATA_FILENAME,index=False, encoding="utf-8")
celebrity_picture_data.to_csv(PICTURE_DATA_FILENAME,index=False, encoding="utf-8")



## Download pictures
ELAPSED = 0
ETA = 999999
START_TIME = time.perf_counter() 
TOTAL_TIME = ETA
PICS_DOWNLOADED = 0
TOTAL_PICS = TOTAL_PICS +1

def download_pictures(URL,PICTURE_LOCATION):
    global PICS_DOWNLOADED, TOTAL_PICS,ELAPSED,ETA
    try:
        wget.download(URL,PICTURE_LOCATION)
        celebrity_picture_data.loc[celebrity_picture_data.picture_link == URL,'downloaded'] = True
    except:
        print("Error downloading " + URL + "\n***"+str(sys.exc_info()))
        celebrity_picture_data.loc[celebrity_picture_data.picture_link == URL,'downloaded'] = False
        
    PICS_DOWNLOADED += 1
    ELAPSED = time.perf_counter() - START_TIME
    TOTAL_TIME = TOTAL_PICS*ELAPSED/PICS_DOWNLOADED
    ETA = TOTAL_TIME-ELAPSED
    print("Downloader: Picture {0} of {1},\t {2} %. \n\tURL = {3}\n\tPics downloaded = {4}.\n\tElapsed = {5}.\n\tTotal time = {6}.\n\tETA = {7}".format(PICS_DOWNLOADED,TOTAL_PICS,100*PICS_DOWNLOADED/TOTAL_PICS,URL,PICS_DOWNLOADED,display_time(ELAPSED),display_time(TOTAL_TIME),display_time(ETA)))

if len(celebrity_pictures_to_download.picture_link) >= 1:
    np.vectorize(download_pictures)(celebrity_pictures_to_download.picture_link.values,PICTURE_LOCATION)
else:
    print("Downloader: No pictures to download.")
celebrity_picture_data.to_csv(PICTURE_DATA_FILENAME,index=False, encoding="utf-8")

print("Total time elapsed: " + display_time(time.perf_counter() - TIME_BEGIN))

input("INFO: Enter to close")