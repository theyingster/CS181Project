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
from bs4 import BeautifulSoup

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
        listOfKDA = soup.findAll('div', {'class':"KDA"})
        listofKills = soup.findAll('span', {'class':"Kill"})
        listofDeaths = soup.findAll('span', {'class':"Death"})
        listofAssists = soup.findAll('span', {'class':"Assist"})
        result = ""
        print(listofKills)

        # parse the ResultSet items into strings
        for kda in listOfKDA:
            result += kda.text.strip() + "\n"
        result += "List of KDAs:\n"
        for i in range(len(listofAssists)):
            result += listofKills[i].text + "\\" + listofDeaths[i].text \
                        + "\\" + listofAssists[i].text + "\n"
        
        return result

    except requests.exceptions.ConnectionError:
        print("\nCONNECTION ERROR - check connection and try again")
    


if True:
    # write BeautifulSoup filtered content to output.txt
    content = get_player_info("theyingster")
    txt = open("output.txt","w")
    txt.write(content)
    txt.close()