#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# first build a functon that gets all of the data from a profile

from bs4 import BeautifulSoup
import requests
from login_function import pbr_login # this imports Atom's login function
import csv

try:
    sess = pbr_login(requests.Session()) # tries to log in
except:
    print("Couldn't log in")

def get_stats(url):
    ranking_list = []
    stat_list = []
    report_list = []
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
        try:
            for stat in soup.find_all("ul", {"class": "data-list"}):
                for naked_stat in stat.find_all("strong"):
                    stat_list.append(naked_stat.text)
        except:
            print("Regular data was not found.") # shouldn't get called
        
        # this chunk gets the reports
        try:
            for stat in soup.find_all("div", {"class": "comment"}):
                report_list.append(stat.text)
        except:    
            print("Report data not found.")

        return stat_list, ranking_list, report_list

    else:
        print("Status Code not 200")

print(get_stats("https://www.prepbaseballreport.com/profiles/NY/Ian-Anderson-9408172536-8451697230#tab2"))

"""
for x in range(len(url_list)):
    get_stats(url_list[x])
"""