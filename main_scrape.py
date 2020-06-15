#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from login_function import pbr_login # this imports Atom's login function

# request test -> works for me...

r = requests.get(
    'https://en.wikipedia.org/wiki/Web_scraping')

if r.status_code == 200:
    soup = BeautifulSoup(r.content, "html.parser")
    
    for headline in soup.find_all("span", {"class": "mw-headline"}):
        print(headline.text)