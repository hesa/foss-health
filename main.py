#!/bin/env python3

import re
from repo import RepoScraperFactory

repo_site="https://github.com"
first="vinland-technology"
repo="flict"
repo_url=f'{repo_site}/{first}/{repo}'

scraper = RepoScraperFactory.RepoScraper(repo_url)
data = scraper.scan_repo()
import json
print("data: " + json.dumps(data, indent=4))
