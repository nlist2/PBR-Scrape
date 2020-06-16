#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# first build a functon that gets all of the data from a profile

from bs4 import BeautifulSoup
import requests
from login_function import pbr_login # this imports Atom's login function
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
            for report in soup.find_all("div", {"class": "comment"}):
                report_list.append(report.text)
        except:    
            print("Report data not found.")

        return stat_list, ranking_list, report_list

    else:
        print("Status Code not 200")

#print(get_stats("https://www.prepbaseballreport.com/profiles/NY/Ian-Anderson-9408172536-8451697230#tab2"))

"""

['2016', 'RHP', 'Shenendehowa', 'NY', '6-3', '170lbs', 'R/R', '95 ', '90-92 ', '78-81 ', '77-79 '], 
['1Rank', '1POS', '3Rank', '2POS'], 
['April 2016', 'Electric showing by Ian, 94-95 MPH with plus life and downhill plane to the  ball. The command was iffy in the first inning, but by inning 3 and 4 he  was spot on. The breaking ball was 77/78 and comes out of his hand like  a fastball, excellent shape to it. Changeup is avg, needs ball rotation  fix. Delivery is clean and his extension out front is outstanding.', 
'Summer 2015', 'Anderson stays hot this summer creating an even bigger buzz than he did this spring. Already committed to Vanderbilt, the lean, lanky righty (6-foot-3, 175-pounds) faced off with some of the top talent spread across the country - and dealt. In one National event (USA 18U NT) he worked 10.1 innings surrendering only one earned run while punching out 15. Now the No. 
1 player in the New York rankings, Anderson has a fastball sitting 90-94 mph with a loose-easy arm action, above average feel for his breaking ball, and shows we can attack hitters with conviction. This will be an extremely big spring for the Albany native.', 'Spring 2014', 'No. 2 in the class of 2016 player rankings is Ian Anderson. Built to pitch, at 6-foot-3,170-pounds, with a frame capable of taking on more weight, 
there is a ton to like about this young pitchers upside. Already the RHP has turned the heat up with the fastball topping an 90 mph two times this summer, sitting consistently 85-87 all day. With a smooth clean, loose easy-arm action there\'s velocity projection to come. Curveball sits 74-77 mph with gradual depth, signs of a high-level pitch. Quality changeup with fastball hand-speed, swing and miss pitch. 
Committed to Vanderbilt, and is arguably the best "pitcher" in the NY Class of 2016 rankings.']

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
