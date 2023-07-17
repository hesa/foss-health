# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from naive_foss_health.scrapers.github import GitHubRepoScraper

FLICT_REPO = "https://github.com/vinland-technology/flict"

def test_class():
    scraper = GitHubRepoScraper(FLICT_REPO)
    assert scraper.__class__.__name__ == "GitHubRepoScraper"

def test_provider():
    scraper = GitHubRepoScraper(FLICT_REPO)
    assert scraper.repo_provider() == "GitHub"

def test_url_expr():
    scraper = GitHubRepoScraper(FLICT_REPO)
    assert scraper.url_expr() == "github.com"

def test_scrape():
    scraper = GitHubRepoScraper(FLICT_REPO)
    scraper.scan_repo()

def test_bad_scrape():
    scraper = GitHubRepoScraper(FLICT_REPO+"-bla-bla")
    with pytest.raises(Exception):
        scraper.scan_repo()
