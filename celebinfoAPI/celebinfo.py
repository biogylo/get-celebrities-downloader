import os
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import json
import datetime

import re
import unicodedata
import html
from importlib import reload
repl = str.maketrans(
    "ÁÉÚÍÓÀÈÙÌÒÄËÜÏÖáéúíóàèùìòäëüïö",
    "AEUIOAEUIOAEUIOaeuioaeuioaeuio"
    )
def nrm(input_string): # Remove diacritics and trailing spaces
    global repl
    return input_string.strip().translate(repl)
def extract(URL):
    HTML_BYTES = requests.get(URL).content
    HTML_STRING = html.unescape(HTML_BYTES.decode("utf-8"))
    #Get name and occupation through regex on the HTML source
    try:
        name,occupation = re.search(u'<h1>([^<>]+)\s\s?<div\sclass="person-title">\s<a href="[^"]*">([^<>]+)</a>',HTML_STRING ).group(1,2)
    except:
        name,occupation = [re.search(u'<h1>([^<>]+)',HTML_STRING )[1],"Not Found"]
        
     #Get birthday through regex on the HTML source
    try:
        birth_month,birth_day,birth_year = re.search(u'<h6>\s?Birthday\s?</h6>\s?\s?<a href="[^"]+"><span class="hidden-sm">([^<>]+)</span><span class="[^"]*">[^<>]+</span>([\d ]+)</a>,\s?<a href="[^"]+">([\d ]+)</a>',HTML_STRING).group(1,2,3)
    except:birth_month,birth_day,birth_year = ["Not found","-1","-1"]
    
    #Get birth city and country through regex on the HTML source
    try:
        birth_city,birth_country = re.search(u'<h6>\s?Birthplace\s?</h6>\s(?:<a href="[^"]*">)?([^<>]+)(?:</a>)?,\s?<a href="[^"]*">([^<>]+)</a>',HTML_STRING).group(1,2)
    except:
        try:
            birth_city,birth_country = re.search(u'<h6>Birthplace</h6>\s<a href="[^"]*">([^<>,]+),\s?([^<>,]+)</a>',HTML_STRING).group(1,2)
        except:
            try:
                birth_city,birth_country = ["Not found",re.search(u'<h6>Birthplace</h6>\s<a href="[^"]*">([^<>,]+)</a>',HTML_STRING)[1]]

            except:
                birth_city,birth_country = ["Not found","Not found"]
                print("error, on " + name + " : " + URL)
                
    #Get age  regex on the HTML source
    try:
        age = re.search(u'<h6>Age </h6><a href="[^"]*">\s?(\d+)',HTML_STRING)[1]
    except:age = "-1"

    #Get birth sign through regex on the HTML source
    try:birth_sign = re.search(u'<h6>Birth Sign\s?</h6><a href="[^"]*">([^<>]+)',HTML_STRING)[1]
    except:birth_sign = "Not Found"

    data = {"url":URL,"name": nrm(name), "occupation": nrm(occupation), "birth_month": nrm(birth_month), "birth_day": int(nrm(birth_day)), "birth_year": int(nrm(birth_year)), "birth_city": nrm(birth_city),"birth_country": nrm(birth_country), "age": int(nrm(age)), "birth_sign": nrm(birth_sign)}
    return data

def from_link(URL):
    # Collecting individual celebrity link
    HTML = requests.get(URL).content
    SOUP = BeautifulSoup(HTML, "html.parser")
    ALL_LINKS = SOUP.find_all('a', 'face person-item clearfix')#'celeb')

    # Variables to store date
    response = {}
    data = []

    # Gettinge data from each links
    

    for each in ALL_LINKS:
        data.append(extract(each['href']))
    return data

def from_day_month(day, month):
	# Collecting individual celebrity link
	URL = "http://www.famousbirthdays.com/" + str(month) + str(day) + ".html"

	return from_link(URL)

def name(celeb_name):
    URL = "http://www.famousbirthdays.com/names/" + celeb_name + ".html"
    HTML = requests.get(URL).content
    SOUP = BeautifulSoup(HTML, "html.parser")

    if SOUP.title.string == "Page Not Found":
        return json.dumps({"error": "Not found"}, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        ALL_LINKS = SOUP.find_all('a', 'celeb')

        # Variables to store date
        response = {}
        data = []

        # Gettinge data from each links
        for each in ALL_LINKS:

            URL = each['href']
            HTML = requests.get(URL).content
            SOUP = BeautifulSoup(HTML, "html.parser")

            try:name = SOUP.find_all('h2')[1].string
            except:name = "Not Found"

            try:photo_url = SOUP.figure.a.img['src']
            except:photo_url = "Not Found"
            
            try:occupation = SOUP.findAll("strong", { "class" : "uppercase" })[0].a.font.span.string
            except:occupation = "Not Found"

            try:birthday = SOUP.findAll("strong", { "class" : "overflow" })[0].time.a.b.font.string
            except:birthday = "Not Found"

            try:birth_year = SOUP.findAll("strong", { "class" : "overflow" })[0].time.find_all('a')[1].b.font.string
            except:birth_year = "Not Found"

            try:birth_place = SOUP.findAll("strong", { "class" : "overflow" })[1].a.b.font.string
            except:birth_place = "Not Found"

            try:age = int((SOUP.findAll("strong", { "class" : "overflow" })[2].b.font.a.font.string).split()[0])
            except:age = "Not Found"

            try:birth_sign = SOUP.findAll("strong", { "class" : "overflow" })[3].a.b.font.string
            except:birth_sign = "Not Found"

            data.append({"name": name, "photo_url": photo_url, "occupation": occupation, "birthday": birthday, "birth_year": birth_year, "birth_place": birth_place, "age": age, "birth_sign": birth_sign})

        # Return json response
        response['data'] = data
        return json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))

