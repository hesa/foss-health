import logging
from naive_foss_health.scrapers.github import GitHubRepoScraper
from naive_foss_health.repo_interface import RepoScraperException


class RepoScraperFactory:

    __supported_scrapers = [ GitHubRepoScraper ]

    @staticmethod
    def supported_scrapers():
        return RepoScraperFactory.__supported_scrapers
    
    @staticmethod
    def RepoScraper(repo):
        for scraper in RepoScraperFactory.__supported_scrapers:
            try:
                logging.debug(f'trying to create {scraper.repo_provider} Scraper')
                return scraper(repo)
            except:
                logging.debug(f'failed creating {scraper.repo_provider} Scraper')

        raise RepoScraperException(f'Could not find a scraper for: {repo}.\n   We have available scrapers for : {[ x.url_expr() for x in RepoScraperFactory.supported_scrapers() ]}' )
