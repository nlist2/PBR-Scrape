#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from login_function import pbr_login
from get_comments import get_comments_new
import csv
import pandas as pd

pbr_urls = pd.read_csv("pbr_urls.csv")
url_list = pbr_urls['plink']

try:
    sess = pbr_login(requests.Session()) # tries to log in
except:
    print("Couldn't log in")

def get_stats(url):
    global stat_list, ranking_list, report_list

    stat_list = []
    report_list = []
    r = sess.get(str(url)) # initiating a session with the account logged in

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")

        # checking to see if the player has a ranked profile
        try:
            rankings = soup.select('.player-rank')
            ranks = {}
            if len(rankings) > 0:
                for rank_n, rank in enumerate(rankings):
                    ranklabel = rank.select_one('.rank-label').text.lower().strip().replace(' ', '_')
            
                    for trsh in rank.select('span'):
                        trsh.decompose()
                    ranks[ranklabel + '_pos_rank'] = rank.select_one('.pos-rank').text.strip()
                    ranks[ranklabel + '_pbr_rank'] = rank.select_one('.pbr-rank').text.strip()
                ranking_list = pd.DataFrame([ranks])

            # de-clogging the function's output
            if(pd.DataFrame([ranks]).empty):
                ranking_list = []
        except:
            print("This player is not ranked.")
        
        # this chunk gets all of the stats available to regular consumers

        sl_df = pd.DataFrame(columns=['Graduating Class', 'Primary Position', 'High School', 'State', 'Height', 'Weight', 'Bat/Throw'])
        # print(sl_df)
        outer_div = soup.find("ul", {"class": "data-list"})
        for stat in outer_div.find_all("li"):
            if("Graduating Class:" in stat.text.replace("\n", "")):
                print(stat.find("strong").text.strip())
                    #sl_df.append(pd.Series(naked_stat.text.strip(), index=sl_df.columns), ignore_index = True)
            if("Primary Position:" in stat.text.replace("\n", "")):
                print(stat.find("strong").text.strip())

            if("High School:" in stat.text.replace("\n", "")):
                print(stat.find("strong").text.strip())

            if("State:" in stat.text.replace("\n", "")):
                print(stat.find("strong").text.strip())

            if("Height:" in stat.text.replace("\n", "")):
                print(stat.find("strong").text.strip())
            
            if("Weight:" in stat.text.replace("\n", "")):
                print(stat.find("strong").text.strip())
            
            if("Bat/Throw:" in stat.text.replace("\n", "")):
                print(stat.find("strong").text.strip())

        return stat_list #, ranking_list #, get_comments_new(url, sess)

    else:
        print("Status Code not 200")

for x in range(len(url_list)):
    print(get_stats(url_list[x]))

"""
with open("pbr_results.csv", "w") as f:
        csvwriter = csv.writer(f)
        headers = ["Grad Year", "Position", "City", "State", "Height", "Weight", "Hand", "Max Fastball", 
        "Avg. Fastball", "Pitch 2", "Pitch 3",
        "State Rank", "State Position Rank", "Overall Rank", "Overall Position Rank",
        "Report"]
        csvwriter.writerow(headers)

for x in range(len(url_list)):
    get_stats(url_list[x])
    with open("pbr_results.csv", "a") as f:
        csvwriter = csv.writer(f)
        content = stat_list + ranking_list + report_list
        csvwriter.writerow(content)
"""