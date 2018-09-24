# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 08:18:24 2018

@author: MWJ
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import re

url = "http://games.espn.com/ffl/schedule?leagueId=133377&teamId=1&seasonId=2011"

chrome_path = r"C:\Users\matth\Desktop\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, "lxml")

table = soup.find('table', attrs={'class':'tableBody'})


def franchise_2011_identification(text):
    if 'Scott' in text:
        return 'Scott & James'
    elif 'Doug' in text:
        return 'Doug'
    elif re.search('\bteamId=3\b', url) is not None:
        return 'Doug'
    elif 'godlegend' in text:
        return 'Crockett'
    elif 'Doyle' in text:
        return 'Garner & Doyle'
    elif 'Fischer' in text:
        return 'Kfish'
    elif 'Kyle' in text:
        return 'Kyle'
    elif 'john gaudet' in text:
        return 'Gaudet & Cameron'
    elif 'Pohlig' in text:
        return 'Gilhop & MJ'
    elif 'Mitch' in text:
        return 'Mitch'
    elif 'Ross' in text:
        return 'Matt & Ross'
    elif re.search('\bteamId=1\b', url) is not None:
        return 'Matt & Ross'
    
def season_identification(text):
    if 'seasonId=2011&amp' in text:
        return 2011
def week_identification(text):
    if 'scoringPeriodId=2&amp' in text: 
        return 2

specify_week = 3  #2 starts us at week 1; so add 1 to every week for this index
cells = []
for table_row in table.findAll("tr"):
    cells.append(table_row.findAll("td"))

all_data_string = str(cells[specify_week][2])
all_numbers_in_string = re.findall(r'\d{1,5}', all_data_string) #good for week, season, homefranchise#
scores = re.findall(r'[0-9]*[\.?][-][0-9]*', all_data_string) #'[0-9]*[.][0-9]' #^[^-]*[^ -] is everything up to the hyphen
entry_number = 1

#for the db
matchup_id = entry_number #increment this somehow
franchise = franchise_2011_identification(url)
season = season_identification(all_data_string)   #all_numbers_in_string[4]
week = week_identification(all_data_string)
points_scored = ''.join(re.findall(r'(?<=W\s|L\s|T\s)[0-9]*[.]?[0-9]', all_data_string)) #the regex outputs a list that needs to be converted to a string with .join
points_against = ''.join(re.findall(r'(?<=-)[0-9]*[.]?[0-9]', all_data_string))
opponent = franchise_2011_identification(str(cells[specify_week]))
week_total = float(points_scored) + float(points_against) #the points have been converted from lists to strings within their own variables, but need to be converted to floats in order to manipulate them mathematically

#assign home team by number from all_numbers_string. if 1 then Matt & Ross, but can change dictionary by the season 

#print(cells[specify_week])

print(franchise, season, week, points_scored, points_against, opponent, week_total)