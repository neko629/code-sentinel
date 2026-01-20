import logging

import requests
from github import Github

from code_sentinel.config import config
from code_sentinel.core.git_provider import GitProvider

logger = logging.getLogger(__name__)

class GitService(GitProvider):

    def __init__(self):
        token = config.GITHUB_TOKEN
        if not token:
            logger.error("GITHUB_TOKEN not set")
            raise ValueError("GITHUB_TOKEN not set")
        self.client = Github(token)

    def get_pr_diff(self, repo_name: str, pr_number: int) -> str:
        """
        get diff
        :param repo_name:
        :param pr_number:
        :return:
        """
        repo = self.client.get_repo(repo_name)
        pr = repo.get_pull(number=pr_number)

        headers = {
            "Authorization": f"token {config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3.diff" # important to get diff format
        }

        response = requests.get(pr.diff_url, headers=headers)
        response.raise_for_status() # raise error if request failed

        return response.text

    def post_comment(self, repo_name: str, pr_number: int, comment: str):
        """
        post comment to pr
        :param repo_name:
        :param pr_number:
        :param comment:
        :return:
        """
        repo = self.client.get_repo(repo_name)
        pr = repo.get_pull(pr_number)

        formatted_comment = f"## Code Review Comments by Code-Sentinel:\n\n{comment}"
        pr.create_issue_comment(formatted_comment)

# singleton     instance
git_service = GitService()

