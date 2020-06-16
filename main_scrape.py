#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# first build a functon that gets all of the data from a profile

from bs4 import BeautifulSoup
import requests
from login_function import pbr_login # this imports Atom's login function
import csv

# request test -> works for me...

sess = pbr_login(requests.Session())
stat_list = []

def get_stats(url)
    r = requests.get(
        url)

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        
        for stat in soup.find_all("ul", {"class": "data-list"}):
            for naked_stat in stat.find_all("strong"):
                stat_list.append(naked_stat.text)

    else:
        print("Status Code not 200")