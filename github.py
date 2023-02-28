from repo_interface import RepoScraper
from web import get_page

import bs4
from bs4 import BeautifulSoup

import re

class GitHubRepoScraper(RepoScraper):

    def __init__(self, repo_url):
        print("GH :)")
        self.repo_url = repo_url.replace("https://github.com","")
        self.index_page = get_page(repo_url)
        self.issues_page = get_page(f'{repo_url}/issues')
        self.pullrequest_page = get_page(f'{repo_url}/pulls')
        
    
    def scan_repo(self):
        print("GH scan_repo")
        data = {}

        # store raw data
        data['raw'] = {}
        data['raw']['index'] = self._scan_index_page(self.index_page)
        data['raw']['pulls'] = self._scan_pulls_page(self.pullrequest_page)
        data['raw']['issues'] = self._scan_issues_page(self.issues_page)

        # format generically
        data['stars'] = data['raw']['index']['stars']
        data['contributors'] = data['raw']['index']['contributors']
        data['watchers'] = data['raw']['index']['watching']
        data['releases'] = data['raw']['index']['releases']
        data['commits'] = data['raw']['index']['commits']
        data['forks'] = data['raw']['index']['forks']
        data['tags'] = data['raw']['index']['tags']
        data['pulls_open'] = data['raw']['pulls']['open']
        data['pulls_closed'] = data['raw']['pulls']['closed']
        data['milestones'] = data['raw']['pulls']['milestones']
        data['labels'] = data['raw']['pulls']['labels']
        data['issues_open'] = data['raw']['issues']['open']
        data['issues_closed'] = data['raw']['issues']['closed']
        
        return data
    

    def _scan_pulls_page(self, page):
        #print("page: " + str(page))
        soup = BeautifulSoup(page, 'html.parser')
        data = {}
        mt2s = soup.find_all(attrs={"class": "mt-2"})

        # closed
        href_str = f"{self.repo_url}/issues?q=is%3Apr+is%3Aclosed"
        closed_str = soup.find_all("a", href=href_str)[1].text
        _closed = re.sub(r"\s+","", closed_str).replace("Closed", "")

        # open
        href_str = f"{self.repo_url}/issues?q=is%3Aopen+is%3Apr"
        open_str = soup.find_all("a", href=href_str)[1].text
        _open = re.sub(r"\s+","", open_str).replace("Open", "")

        # milestones
        href_str = f"{self.repo_url}/milestones"
        milestones_str = soup.find_all("a", href=href_str)[1].text
        _milestones = re.sub(r"\s+","", milestones_str).replace("Milestones", "")

        # labels
        href_str = f"{self.repo_url}/labels"
        labels_str = soup.find_all("a", href=href_str)[1].text
        _labels = re.sub(r"\s+","", labels_str).replace("Labels", "")

        data['closed'] = _closed
        data['open'] = _open
        data['milestones'] = _milestones
        data['labels'] = _labels
        return data
        
    def _scan_issues_page(self, page):
        #print("page: " + str(page))
        soup = BeautifulSoup(page, 'html.parser')
        data = {}
        mt2s = soup.find_all(attrs={"class": "mt-2"})

        # closed
        href_str = f"{self.repo_url}/issues?q=is%3Aissue+is%3Aclosed"
        closed_str = soup.find_all("a", href=href_str)[1].text
        _closed = re.sub(r"\s+","", closed_str).replace("Closed", "")

        # open
        href_str = f"{self.repo_url}/issues?q=is%3Aopen+is%3Aissue"
        open_str = soup.find_all("a", href=href_str)[1].text
        _open = re.sub(r"\s+","", open_str).replace("Open", "")

        # milestones
        href_str = f"{self.repo_url}/milestones"
        milestones_str = soup.find_all("a", href=href_str)[1].text
        print("milestones_str: " + milestones_str)
        _milestones = re.sub(r"\s+","", milestones_str).replace("Milestones", "")

        # labels
        href_str = f"{self.repo_url}/labels"
        labels_str = soup.find_all("a", href=href_str)[1].text
        print("labels_str: " + labels_str)
        _labels = re.sub(r"\s+","", labels_str).replace("Labels", "")

        data['closed'] = _closed
        data['open'] = _open
        data['milestones'] = _milestones
        data['labels'] = _labels
        return data
        
    def _scan_index_page(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        data = {}
        mt2s = soup.find_all(attrs={"class": "mt-2"})
        for m in mt2s:
            alist = m.find_all("a", class_="Link--muted")
            for a in alist:
                #print(f'   -- a {a}')
                #print(f'       -- c len: {len(a.contents)}')
                if len(a.contents) > 3:
                    value = a.contents[3].text
                    variable = a.contents[4].strip()
                    print(f'       -- value:     {value}')
                    print(f'       -- variable:  {variable}')
                    data[variable] = value

        alist = soup.find_all("a", id="issues-tab")
        #print(f' issues :  "{alist[0].text.replace("Issues","").strip()}"')
        data["issues"] = alist[0].text.replace("Issues","").strip()

        brlist = soup.find_all("a", href=f"{self.repo_url}/branches")
        #print(f' Br :  "{brlist[1].text.replace("branches","").strip()}"')
        data["branches"] = brlist[1].text.replace("branches","").strip()
        
        taglist = soup.find_all("a", href=f"{self.repo_url}/tags")
        #print(f' Tag :  "{taglist[1].text.replace("tags","").replace("tag","").strip()}"')
        data["tags"] = taglist[1].text.replace("tags","").replace("tag","").strip()
        
        rellist = soup.find_all("a", href=f"{self.repo_url}/releases")
        #print(f' Rel :  "{rellist[0].text.replace("Releases","").strip()}"')
        data["releases"] = rellist[0].text.replace("Releases","").strip()
        
        forklist = soup.find_all("a", href=f"{self.repo_url}/network/members")
        #print(f' Fork :  "{forklist[1].text.replace("forks","").replace("fork","").strip()}"')
        data["forks"] = forklist[1].text.replace("forks","").replace("fork","").strip()

        watchlist = soup.find_all("a", href=f"{self.repo_url}/watchers")
        #print(f' Watch :  "{watchlist[0].text.replace("watching","").strip()}"')
        data['watchers'] = watchlist[0].text.replace("watching","").strip()
        
        starlist = soup.find_all("a", href=f"{self.repo_url}/stargazers")
        #print(f' Stars :  "{starlist[0].text.replace("stars","").replace("star","").strip()}"')
        data["stars"] = starlist[0].text.replace("stars","").replace("star","").strip()
        
        comlist = soup.find_all("a", href=f"{self.repo_url}/commits/main")
        #print(f' Commits :  "{comlist[0].text.replace("commits","").replace("commit","").strip()}"')
        data["commits"] = comlist[0].text.replace("commits","").replace("commit","").strip()


        contrlist = soup.find_all("a", href=f"{self.repo_url}/graphs/contributors")
        print(f' Contributors :  "{contrlist[0].text.replace("commits","").replace("commit","").strip()}"')
        data["contributors"] = contrlist[0].text.replace("Contributors","").strip()


        
        return data
