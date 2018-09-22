# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 11:47:09 2018

@author: MWJ
"""

#from selenium import webdriver
#chrome_path = r"C:\Users\matth\Desktop\chromedriver_win32\chromedriver.exe"
#driver = webdriver.Chrome(chrome_path)

#url = "http://games.espn.com/ffl/schedule?leagueId=133377&teamId=1&seasonId=2017" 

#driver.get(url)
#items = driver.find_elements_by_css_selector("td")


from bs4 import BeautifulSoup
from selenium import webdriver

schedule_url = "http://games.espn.com/ffl/schedule?leagueId=133377&teamId=1&seasonId=2017"
boxscore_url = "http://games.espn.com/ffl/boxscorequick?leagueId=133377&teamId=6&scoringPeriodId=1&seasonId=2017&view=scoringperiod&version=quick"

chrome_path = r"C:\Users\matth\Desktop\chromedriver_win32\chromedriver.exe"
#driver = webdriver.Chrome(chrome_path)


#driver.get(boxscore_url)

#html = driver.page_source
#soup = BeautifulSoup(html, "lxml")

#for tag in soup.find_all("td"):
 #   print (tag.text)
    
#table = soup.find("table", {"class" : "playerTableTable tableBody" })
#for row in table.findAll("tr"):
#    cells = row.findAll("td")
#    print(cells)
    
    
import pymysql
con = pymysql.connect('localhost', 'root', 
    'SundayFunday7', 'fantasystats')
#with con: 
#    cur = con.cursor()
#    cur.execute("SELECT VERSION()")

#    version = cur.fetchone()
    
#    print("Database version: {}".format(version[0]))
#column1 = 'franchise'
#column2 = 'points_scored'
#value1 = 'Mitch'
#value2 = 125.67

dynamic_id = 4
result = 0

cursor = con.cursor()
#cursor.execute("""DROP TABLE matchuptable;""")
cursor.execute("""INSERT INTO matchuptable
VALUES(%i, 'Matt & Ross', 2018, 3, 'Gaudet & Cameron', 151.310, 129.910, 0;""" % dynamic_id)
con.commit()

### Saturday: 1. How to map a variable from python into the SQL command, 2. compute variables on the fly -- compute margin given points scored and against, and insert margin into the db
#print(cursor.fetchall())

#cursor.execute("""INSERT INTO matchuptable VALUES (%s)""",(18800))
#con.commit()

con.close()
print('done') 