class RepoScraper:

    def __init__(self, repo_url):
        return None
    
    def scan_repo(self):
        return None

    @staticmethod
    def url_expr():
        return None

    @staticmethod
    def repo_provider():
        return None


class RepoScraperException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

