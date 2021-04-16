#
# final project ~ CS 181 spring 2021
#

#
# Name(s): Vivian Pou, Wayne Ying
#

# simple API - http://lol.lukegreen.xyz/
# op gg scraper - https://github.com/jlgre/opgg_scraper
# https://pypi.org/project/scrapeGG/

import requests
import string
import json
import time
import os

from bs4 import BeautifulSoup

sup = [""]
adc = [""]
mid = [""]
jung = [""]
top = [""]

roles = [sup, adc, mid, jung, top] # support, adc, mid, jung, top




def get_player_champion_info(username):
    username = username.replace(" ","+").lower()
    champion_url = f"https://na.op.gg/summoner/champions/userName={username}"

    try:    
        response = requests.get(champion_url)   # request the page
        print(champion_url)

        if response.status_code == 404:                 # page not found
            print("There was a problem with getting the page:")
            print(champion_url)

        data_from_url = response.text                  # the HTML text from the page
        soup = BeautifulSoup(data_from_url, "lxml")
        
        # class = GameDetail (outer div tag for each game)
        listofRatios = soup.findAll('span', {'class':"WinRatio"})
        listofWins = soup.findAll('div', {'class':"Text Left"})
        w = 0
        listofLosses = soup.findAll('div', {'class':"Text Right"})
        l = 0
        listofKills = soup.findAll('span', {'class':"Kill"})
        listofDeaths = soup.findAll('span', {'class':"Death"})
        listofAssists = soup.findAll('span', {'class':"Assist"})
        result = "Kills/Deaths/Assists/Wins/Losses\n"

        for i in range(len(listofAssists)):
            win,loss = ["",""]
            if listofRatios[i].text == "100%":
                l -= 1
                loss = "0"
                win = listofWins[w].text[:-1]
            
            elif listofRatios[i].text == "0%":
                w -= 1
                win = "0"
                loss = listofLosses[l].text[:-1]
            
            else:
                win = listofWins[w].text[:-1]
                loss = listofLosses[l].text[:-1]

            result += listofKills[i].text + "/" + listofDeaths[i].text \
                        + "/" + listofAssists[i].text + "/" + win \
                            + "/" + loss + "\n"
            w += 1
            l += 1
        
        return result

    except requests.exceptions.ConnectionError:
        print("\nCONNECTION ERROR - check connection and try again")

def get_player_info(username):
    """ This function requests the player information (currently KDA
        for each game) and parses it with Beautiful Soup, returning 
        the resulting Beautiful Soup object in string form for writing
        into output text file.
    """
    username = username.replace(" ","+").lower()
    player_url = f"https://na.op.gg/summoner/userName={username}"
    try:    
        response = requests.get(player_url)   # request the page
        print(player_url)

        if response.status_code == 404:                 # page not found
            print("There was a problem with getting the page:")
            print(player_url)

        data_from_url = response.text                  # the HTML text from the page
        soup = BeautifulSoup(data_from_url, "lxml")
        
        # class = GameDetail (outer div tag for each game)
        listofKills = soup.findAll('span', {'class':"Kill"})
        listofDeaths = soup.findAll('span', {'class':"Death"})
        listofAssists = soup.findAll('span', {'class':"Assist"})
        result = ""
        #print(listofKills)

        # parse the ResultSet items into strings
        # for kda in listOfKDA:
        #     result += kda.text.strip() + "\n"
        result += "Kills/Deaths/Assists\n"
        j = 0
        for i in range(len(listofAssists)):
            if i < 8:
                j += 1
                continue
            if "Kill" in listofKills[j].text:
                j += 1
            result += listofKills[j].text + "/" + listofDeaths[i].text \
                        + "/" + listofAssists[i].text + "\n"
            j += 1
        
        return result

    except requests.exceptions.ConnectionError:
        print("\nCONNECTION ERROR - check connection and try again")

if True:
    # write BeautifulSoup filtered content to output.txt
    content = get_player_info("theyingster")
    txt = open("output.txt","w")
    txt.write(content)
    txt.close()

    champions = get_player_champion_info("theyingster")
    txt = open("champions.txt","w")
    txt.write(champions)
    txt.close()

    f = open("output.txt", "r")
    with open("player.csv", 'w') as csvFile:
        lines = f.readlines()
        for line in lines:
            csvFile.write(line.replace("/", ","))
    f.close()

    f = open("champions.txt", "r")
    with open("champions.csv", 'w') as csvFile:
        lines = f.readlines()
        for line in lines:
            csvFile.write(line.replace("/", ","))
    f.close()
