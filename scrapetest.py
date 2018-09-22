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
    if 'Doug' in text:
        return 'Doug'
    if 'godlegend' in text:
        return 'Crockett'
    if 'Doyle' in text:
        return 'Garner & Doyle'
    if 'Fischer' in text:
        return 'Kfish'
    if 'Kyle' in text:
        return 'Kyle'
    if 'john gaudet' in text:
        return 'Gaudet & Cameron'
    if 'Pohlig' in text:
        return 'Gilhop & MJ'
    if 'Mitch' in text:
        return 'Mitch'
    if 'Ross' or 'teamId=1&amp' in text:
        return 'Matt & Ross'
    

specify_week = 3  #2 starts us at week 1; so add 1 to every week for this index
cells = []
for table_row in table.findAll("tr"):
    cells.append(table_row.findAll("td"))

all_data_string = str(cells[specify_week][2])
all_numbers_in_string = re.findall(r'\d{1,5}', all_data_string) #good for week, season, homefranchise#
scores = re.findall(r'[0-9]*[.][0-9]', all_data_string)
entry_number = 1

#for the db
matchup_id = entry_number #increment this somehow
franchise = franchise_2011_identification(str(cells[specify_week][2]))
season = all_numbers_in_string[4]
week = all_numbers_in_string[3]
points_scored = scores[0]
points_against = scores[1] # !! list index out of range - these indices must be changing by the week
opponent = franchise_2011_identification(str(cells[specify_week][-1]))
week_total = float(points_scored) + float(points_against) 

#assign home team by number from all_numbers_string. if 1 then Matt & Ross, but can change dictionary by the season 

print(scores)
#print(franchise, season, week, points_scored, points_against, opponent, week_total)
