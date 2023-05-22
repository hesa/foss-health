
import logging
import re

import bs4
from bs4 import BeautifulSoup

from naive_foss_health.web import get_page
from naive_foss_health.repo_interface import RepoScraper
from naive_foss_health.repo_interface import RepoScraperException

GITHUB_DOMAIN_EXPR = "github.com"

class GitHubRepoScraper(RepoScraper):

    
    def __init__(self, repo_url):
        logging.debug(f'GH  {repo_url}: {GITHUB_DOMAIN_EXPR in repo_url}')
        if GITHUB_DOMAIN_EXPR in repo_url:
            logging.debug('GH looks promising')
            self.repo_url = repo_url.replace("https://github.com","").replace(".git","")
            self.repo_url_full = f'https://{GITHUB_DOMAIN_EXPR}/{self.repo_url}'
            self.index_page = get_page(f'{self.repo_url_full}')
            self.issues_page = get_page(f'{self.repo_url_full}/issues')
            self.pullrequest_page = get_page(f'{self.repo_url_full}/pulls')
            logging.debug('GH created repo scraper for {repo_url}')
        else:
            logging.debug(f'GH FAILED creating repo scraper for {repo_url} since only {GITHUB_DOMAIN_EXPR} is supported by this scraper')
            raise RepoScraperException(f'GitHubRepoScraperCould does not support {repo_url}')


    @staticmethod
    def url_expr():
        return "github.com"

    @staticmethod
    def repo_provider():
        return "GitHub"

    def scan_repo(self):
        logging.debug("GH scan_repo()")
        data = {}

        # store raw data
        data['raw'] = {}

        # scan/scrape pages
        index = self._scan_index_page(self.index_page)
        pulls = self._scan_pulls_page(self.pullrequest_page)
        issues = self._scan_issues_page(self.issues_page)

        # store raw data
        data['raw']['index'] = index
        data['raw']['pulls'] = pulls
        data['raw']['issues'] = issues

        # create generic structure
        data['repository'] = self.repo_url
        data['stars'] = index['stars']
        data['branch'] = index['branch']
        data['contributors'] = index['contributors']
        data['watchers'] = index['watching']
        data['releases'] = index['releases']
        data['commits'] = index['commits']
        data['forks'] = index['forks']
        data['tags'] = index['tags']
        data['pulls_open'] = pulls['open']
        data['pulls_closed'] = pulls['closed']
        data['milestones'] = pulls['milestones']
        data['labels'] = pulls['labels']
        data['issues_open'] = issues['open']
        data['issues_closed'] = issues['closed']
        
        return data
    

    def _scan_pulls_page(self, page):
        #print("page: " + str(page))
        soup = BeautifulSoup(page, 'html.parser')
        data = {}
        mt2s = soup.find_all(attrs={"class": "mt-2"})

        # closed
        href_str = f"{self.repo_url}/issues?q=is%3Apr+is%3Aclosed"
        closed_str = soup.find_all("a", href=href_str)
        _closed = self._soup_extract(closed_str, ["Closed"], default=0, regexp=r"\s+")

        # open
        href_str = f"{self.repo_url}/issues?q=is%3Aopen+is%3Apr"
        open_str = soup.find_all("a", href=href_str)
        _open = self._soup_extract(open_str, ["Open"], default=0, regexp=r"\s+")

        # milestones
        href_str = f"{self.repo_url}/milestones"
        milestones_str = soup.find_all("a", href=href_str)
        _milestones = self._soup_extract(milestones_str, ["Milestones"], default=0, regexp=r"\s+")

        # labels
        href_str = f"{self.repo_url}/labels"
        labels_str = soup.find_all("a", href=href_str)
        _labels = self._soup_extract(labels_str, ["Labels"], default=0, regexp=r"\s+")
        
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
        closed_str = soup.find_all("a", href=href_str)
        _closed = self._soup_extract(closed_str, ["Closed"], default=0, regexp=r"\s+")

        # open
        href_str = f"{self.repo_url}/issues?q=is%3Aopen+is%3Aissue"
        open_str = soup.find_all("a", href=href_str)
        _open = self._soup_extract(open_str, ["Open"], default=0, regexp=r"\s+")

        # milestones
        href_str = f"{self.repo_url}/milestones"
        milestones_str = soup.find_all("a", href=href_str)[1].text
        _milestones = self._soup_extract(milestones_str, ["Milestones"], default=0, regexp=r"\s+")

        # labels
        href_str = f"{self.repo_url}/labels"
        labels_str = soup.find_all("a", href=href_str)[1].text
        _labels = self._soup_extract(labels_str, ["Labels"], default=0, regexp=r"\s+")

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
                    #print(f'       -- value:     {value}')
                    #print(f'       -- variable:  {variable}')
                    data[variable] = value

        alist = soup.find_all("a", id="issues-tab")
        data["issues"] = alist[0].text.replace("Issues","").strip()

        brlist = soup.find_all("a", href=f"{self.repo_url}/branches")
        data["branches"] = brlist[1].text.replace("branches","").strip()
        
        taglist = soup.find_all("a", href=f"{self.repo_url}/tags")
        data["tags"] = taglist[1].text.replace("tags","").replace("tag","").strip()
        
        rellist = soup.find_all("a", href=f"{self.repo_url}/releases")
#        data["releases"] = rellist[0].text.replace("Releases","").strip()
        data["releases"] = self._soup_extract(rellist, ["Releases"])
        
        forklist = soup.find_all("a", href=f"{self.repo_url}/network/members")
        data["forks"] = self._soup_extract(forklist, ["forks", "fork"])

        watchlist = soup.find_all("a", href=f"{self.repo_url}/watchers")
        data['watchers'] = watchlist[0].text.replace("watching","").strip()
        
        starlist = soup.find_all("a", href=f"{self.repo_url}/stargazers")
        data["stars"] = starlist[0].text.replace("stars","").replace("star","").strip()

        spans = soup.find_all("span", {'class' : 'css-truncate-target'})
        for span in spans:
            if span.has_attr('data-menu-button'):
                branch_name = span.text
                break
        
        comlist = soup.find_all("a", href=f"{self.repo_url}/commits/{branch_name}")
        data["commits"] = comlist[0].text.replace("commits","").replace("commit","").strip()

        contrlist = soup.find_all("a", href=f"{self.repo_url}/graphs/contributors")
        data["contributors"] = self._soup_extract(contrlist, ["Contributors"], default=1)
        
        data['branch'] = branch_name

        
        return data

    def _soup_extract(self, datalist, replaces, strip=True, default=0, regexp=None):
        try:
            data = datalist[0].text
            if regexp:
                data = re.sub(regexp, "", data)
            for replace in replaces:
                data = data.replace(replace,"")
            if strip:
                data = data.strip()
            if data == '':
                data = default
            return data
        except Exception as e:
            logging.debug(f"Exception when parsing {datalist}: {e}")
            return default
