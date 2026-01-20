from abc import ABC, abstractmethod


class GitProvider(ABC):
    """Abstract base class for Git providers."""

    @abstractmethod
    def get_pr_diff(selfself, repo_name: str, pr_number: int) -> str:
        """Get the diff of a pull request."""
        pass

    @abstractmethod
    def post_comment(self, repo_name: str, pr_number: int, comment: str):
        """Post a comment on a pull request."""
        pass
