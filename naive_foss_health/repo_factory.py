import logging
from naive_foss_health.scrapers.github import GitHubRepoScraper

class RepoScraperFactory:

    @staticmethod
    def RepoScraper(repo):
        logging.debug("create GitHub Scraper")
        return GitHubRepoScraper(repo)
