#!/bin/env python3

import re
from web import get_page
import bs4
from bs4 import BeautifulSoup

first="vinland-technology"
repo="flict"
repo_url=f'/{first}/{repo}'
index_page = get_page(f'https://github.com/{first}/{repo}')
issues_page = get_page(f'https://github.com/{first}/{repo}/issues')
pullrequest_page = get_page(f'https://github.com/{first}/{repo}/pulls')

def scan_index_page(page):
    soup = BeautifulSoup(page, 'html.parser')
    print(' --- analysing --- ')
    mt2s = soup.find_all(attrs={"class": "mt-2"})
    for m in mt2s:
        #print(f' -- m {m}')
        alist = m.find_all("a", class_="Link--muted")
        for a in alist:
            #print(f'   -- a {a}')
            #print(f'       -- c len: {len(a.contents)}')
            if len(a.contents) > 3:
                value = a.contents[3].text
                variable = a.contents[4].strip()
                print(f'       -- value:     {value}')
                #print(f'       -- c3 {value.strip()}')
                print(f'       -- variable:  {variable}')

    alist = soup.find_all("a", id="issues-tab")
    print(f' issues :  "{alist[0].text.replace("Issues","").strip()}"')

    brlist = soup.find_all("a", href=f"{repo_url}/branches")
    print(f' Br :  "{brlist[1].text.replace("branches","").strip()}"')

    taglist = soup.find_all("a", href=f"{repo_url}/tags")
    print(f' Tag :  "{taglist[1].text.replace("tags","").replace("tag","").strip()}"')

    rellist = soup.find_all("a", href=f"{repo_url}/releases")
    print(f' Rel :  "{rellist[0].text.replace("Releases","").strip()}"')

    forklist = soup.find_all("a", href=f"{repo_url}/network/members")
    print(f' Fork :  "{forklist[1].text.replace("forks","").replace("fork","").strip()}"')

    watchlist = soup.find_all("a", href=f"{repo_url}/watchers")
    print(f' Watch :  "{watchlist[0].text.replace("watching","").strip()}"')

    starlist = soup.find_all("a", href=f"{repo_url}/stargazers")
    print(f' Stars :  "{starlist[0].text.replace("stars","").replace("star","").strip()}"')

    comlist = soup.find_all("a", href=f"{repo_url}/commits/main")
    print(f' Commits :  "{comlist[0].text.replace("commits","").replace("commit","").strip()}"')

scan_index_page(index_page)
