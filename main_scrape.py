#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from login_function import pbr_login # this imports Atom's login function

# request test -> works for me...

r = requests.get(
    'https://www.prepbaseballreport.com/profile-search-results')

if r.status_code == 200:
    soup = BeautifulSoup(r.content, "html.parser")
    
    for headline in soup.find_all("tr", {"class": "alt"}):
        print(headline.text)

    for player in soup.find_all("tr"):
        print(player.text)
        
    print(len(headline), len(player))
else:
    print("failed")