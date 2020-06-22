# -*- coding: utf-8 -*-
"""
@title: ArtistScraper
@description: Downloads a ton of celebrity pictures from celebnames.com
@date:  Thu Jun 18 14:18:58 2020

@author: Juan Francisco Navarro
@email: navarro.juan@uabc.edu.mx

"""
import sys
import datetime
import celebinfoAPI.celebinfo as celeb
from BasicFunctions import display_time
import time
MONTHS = [0,"january","february","march","april","may","june","july","august","september","october","november","december"]

special = [
"https://www.famousbirthdays.com/profession/from/actress-mexico.html",
"https://www.famousbirthdays.com/profession/from/actor-mexico.html",
"https://www.famousbirthdays.com/birthplace/mexico.html",
"https://www.famousbirthdays.com/profession/from/worldleader-mexico.html",
"https://www.famousbirthdays.com/profession/from/singer-mexico.html",
"https://www.famousbirthdays.com/profession/rapper.html",
"https://www.famousbirthdays.com/profession/tvactress.html",
"https://www.famousbirthdays.com/profession/tvactor.html",
"https://www.famousbirthdays.com/profession/movieactress.html",
"https://www.famousbirthdays.com/profession/movieactor.html",
"https://www.famousbirthdays.com/profession/randbsinger.html",
"https://www.famousbirthdays.com/profession/model.html",
"https://www.famousbirthdays.com/profession/wrestler.html",
"https://www.famousbirthdays.com/profession/director.html",
"https://www.famousbirthdays.com/profession/youtubestar.html",
"https://www.famousbirthdays.com/profession/dancer.html",
"https://www.famousbirthdays.com/profession/basketballplayer.html",
"https://www.famousbirthdays.com/profession/rapper.html",
"https://www.famousbirthdays.com/profession/reggaetonsinger.html",
"https://www.famousbirthdays.com/profession/comedian.html",
"https://www.famousbirthdays.com/profession/movieactor.html",
"https://www.famousbirthdays.com/profession/movieactress.html",
"https://www.famousbirthdays.com/profession/gender/popsinger-male.html",
"https://www.famousbirthdays.com/profession/gender/popsinger-female.html"
"https://www.famousbirthdays.com/profession/instagramstar.html",
"https://www.famousbirthdays.com/profession/realitystar.html",
"https://www.famousbirthdays.com/profession/familymember.html",
"https://www.famousbirthdays.com/profession/rocksinger.html",
"https://www.famousbirthdays.com/profession/tvshowhost.html",
"https://www.famousbirthdays.com/profession/entrepreneur.html",
"https://www.famousbirthdays.com/profession/worldmusicsinger.html",
"https://www.famousbirthdays.com/profession/tiktokstar.html",
"https://www.famousbirthdays.com/most-popular-people.html",
"https://www.famousbirthdays.com/astrology/aquarius.html",
"https://www.famousbirthdays.com/astrology/aries.html",
"https://www.famousbirthdays.com/astrology/cancer.html",
"https://www.famousbirthdays.com/astrology/capricorn.html",
"https://www.famousbirthdays.com/astrology/gemini.html",
"https://www.famousbirthdays.com/astrology/leo.html",
"https://www.famousbirthdays.com/astrology/libra.html",
"https://www.famousbirthdays.com/astrology/pisces.html",
"https://www.famousbirthdays.com/astrology/sagittarius.html",
"https://www.famousbirthdays.com/astrology/scorpio.html",
"https://www.famousbirthdays.com/astrology/taurus.html",
"https://www.famousbirthdays.com/astrology/virgo.html"
]
def number_to_date(number):
    date = datetime.date(2020,1,1) + datetime.timedelta(number%366)
    return date



def get_artist_links(TOP = 10,START = 0,TO = 2):
    FROM = START
    
    celebrity_list = []
    
    CATEGORIES = len(special)
    ### Getting by category
    ELAPSED = 0
    ETA = 999999
    START_TIME = time.perf_counter() 
    TOTAL_TIME = ETA
    for INDEX, category in enumerate(special[0:1]):
        date = number_to_date(FROM)
        try:
            celebrity_list.extend(celeb.from_link(category))
            
            ELAPSED = time.perf_counter() - START_TIME
            TOTAL_TIME = (CATEGORIES)*ELAPSED/(INDEX+1)
            ETA = TOTAL_TIME-ELAPSED
            
            GOTTEN = len(celebrity_list)
            print("ArtistScraper: Category {0} of {1},\t {2} %. \n\tLinks got = {3}\n\tElapsed = {4}.\n\tTotal time = {5}.\n\tETA = {6}".format(INDEX,CATEGORIES,100*(INDEX+1)/(CATEGORIES),GOTTEN,display_time(ELAPSED),display_time(TOTAL_TIME),display_time(ETA)))
    
        except:
            print("Failed to do, error in category: " + str(FROM) + ", INDEX: " + str(INDEX) +"\n" + "".join(str(sys.exc_info()))+"\n")

    ### Getting by birthday

    ELAPSED = 0
    ETA = 999999
    START_TIME = time.perf_counter() 
    TOTAL_TIME = ETA
    while FROM < TO:
        date = number_to_date(FROM)
        try:
            celebrity_list.extend(celeb.from_day_month(date.day,MONTHS[date.month])[0:TOP])
            FROM += 1
            ELAPSED = time.perf_counter() - START_TIME
            TOTAL_TIME = (TO-START)*ELAPSED/(FROM-START)
            ETA = TOTAL_TIME-ELAPSED
            
            GOTTEN = len(celebrity_list)
            print("Progress: Day {0} of {1},\t {2} %. \n\tLinks got = {3}\n\tElapsed = {4}.\n\tTotal time = {5}.\n\tETA = {6}".format(FROM-1,TO,100*(FROM-START)/(TO-START),GOTTEN,display_time(ELAPSED),display_time(TOTAL_TIME),display_time(ETA)))
            
        except:
            print("Failed to do, error in day: " + str(FROM)+"\n"+"".join(str(sys.exc_info()))+"\n")

    return celebrity_list