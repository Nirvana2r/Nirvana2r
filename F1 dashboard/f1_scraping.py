# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 03:14:44 2022

@author: nirva
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time


# url of the f1 website 



year = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
 
################# First scraping #################

def scrape_team(url):
    #scrapes the page at the url and returns a dataframe
    page = requests.get(url)
    html = BeautifulSoup(page.content, "html.parser") #page.content is the HTML file. By using the HTML parser we read it as HTML
    
    #get all the HTML fragments with descriptions
    team_html = html.find_all(class_="dark bold uppercase ArchiveLink") 
    pts_html = html.find_all(class_="dark bold")
    
    
    #create an empty list to put in texts of description
    team_list = [] 
    pts_list = []
    
    
    #loop over HTML elements, get text and add to list 
    for i in team_html:
        text = i.text.strip() #use .strip() string method to remove whitespace
        team_list.append(text)
    
    for i in pts_html:
        text = i.text.strip()
        pts_list.append(text)
               
    #make a dictionary with column names for data to put in DataFrame    
    data = {"team": team_list,
            "pts": pts_list}
    
    #create DataFrame
    df = pd.DataFrame(data)  
    return df

#create an empty dataframe
df_team = pd.DataFrame() 

for i in range(len(year)):
    time.sleep(1)
    base_url = "https://www.formula1.com/en/results.html/"+ str(year[i])+ "/team.html"
    df_page = scrape_team(base_url) #use scrape function to get df for the page
    df_page['year'] = year[i]
    df_team = pd.concat([df_team, df_page], ignore_index=True) #concatenate the total df and page df. ignore_index resets index. Only use this if index is meaningless
    print(base_url)
    
    # Cleaning data using rename() because the teams change their names though the years
    # df_team["team"] = df_team["team"].str.replace('Red Bull Racing TAG Heuer', 'Red Bull Racing Honda')
    df_team["team"] = df_team["team"].replace(dict.fromkeys(['Red Bull Racing TAG Heuer', 'Red Bull Racing Renault'], 'Red Bull Racing Honda'))
    df_team["team"] = df_team["team"].replace(dict.fromkeys(['McLaren Renault', 'McLaren Honda'], 'McLaren Mercedes'))
    df_team["team"] = df_team["team"].replace(dict.fromkeys(['Renault', 'Lotus Renault', 'Lotus Mercedes'], 'Alpine Renault'))
    df_team["team"] = df_team["team"].replace(dict.fromkeys(['Scuderia Toro Rosso Honda', 'Toro Rosso', 'STR Ferrari', 'STR Renault','Toro Rosso Ferrari'], 'AlphaTauri Honda'))
    df_team["team"] = df_team["team"].replace(dict.fromkeys(['Racing Point BWT Mercedes', 'Force India Mercedes'], 'Aston Martin Mercedes'))
    df_team["team"] = df_team["team"].replace(dict.fromkeys(['Sauber Ferrari'], 'Alfa Romeo Racing Ferrari'))
    df_team["team"] = df_team["team"].replace(dict.fromkeys(['Williams Renault'], 'Williams Mercedes'))
    #filtering out non existing teams
    df_team = df_team[df_team['team'] != ('Force India Sahara')]
    df_team = df_team[df_team['team'] != 'Marussia Cosworth']
    df_team = df_team[df_team['team'] != 'Caterham Renault']
    df_team = df_team[df_team['team'] != 'HRT Cosworth']
    df_team = df_team[df_team['team'] != 'MRT Mercedes']
    df_team = df_team[df_team['team'] != 'Marussia Ferrari']
    

#df_team.to_csv('df_team')
################# End of First scraping #################

################# Seconde scraping #################
#2022

fastest1 = pd.read_html("https://www.formula1.com/en/results.html/2021/fastest-laps.html")
fastest1 = fastest1[0]

df_fast1 = fastest1[["Grand Prix", "Car", "Time"]]
df_fast1 = df_fast1.sort_values(by='Time', ascending=False)

#2021
fastest2 = pd.read_html("https://www.formula1.com/en/results.html/2020/fastest-laps.html")
fastest2 = fastest2[0]

df_fast2 = fastest2[["Grand Prix", "Car", "Time"]]
df_fast2 = df_fast2.sort_values(by='Time', ascending=False)
#df_fast['year'] = 2021

#2020
fastest3 = pd.read_html("https://www.formula1.com/en/results.html/2019/fastest-laps.html")
fastest3 = fastest3[0]

df_fast3 = fastest3[["Grand Prix", "Car", "Time"]]
df_fast3 = df_fast3.sort_values(by='Time', ascending=False)

################# End of second scraping #################
