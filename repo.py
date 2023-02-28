import github

class RepoScraperFactory:

    @staticmethod
    def RepoScraper(repo):
        print("create GH")
        return github.GitHubRepoScraper(repo)
