#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# first build a functon that gets all of the data from a profile

from bs4 import BeautifulSoup
import requests
from login_function import pbr_login # this imports Atom's login function
import csv

# request test -> works for me...

sess = pbr_login(requests.Session())


def get_stats(url):
    ranking_list = []
    stat_list = []
    r = sess.get(str(url)) # initiating a session with the account logged in

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")

        # checking to see if the player has a ranked profile
        try:
            for stat in soup.find_all("a", {"class": "player-rank"}):
                for rank in stat.find_all("div"):
                    ranking_list.append(rank.text)
        except:
            print("This player is not ranked.")
        
        # this chunk gets all of the stats available to regular consumers
        for stat in soup.find_all("ul", {"class": "data-list"}):
            for naked_stat in stat.find_all("strong"):
                stat_list.append(naked_stat.text)

        return stat_list, ranking_list     

    else:
        print("Status Code not 200")

print(get_stats("https://www.prepbaseballreport.com/profiles/NY/Jon-Melarczik-9624573108#tab5"))