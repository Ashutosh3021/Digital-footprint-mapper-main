"""
Collectors Package

This package contains modules for collecting data from various platforms:
- GitHub
- LinkedIn
- Twitter
- Reddit
- Facebook
- Instagram
- YouTube
- Email
"""

# Import collector classes for easy access
from .github_collector import GitHubCollector
from .linkedin_collector import LinkedInCollector
from .twitter_collector import TwitterCollector
from .reddit_collector import RedditCollector
from .facebook_collector import FacebookCollector
from .instagram_collector import InstagramCollector
from .youtube_collector import YouTubeCollector
from .email_collector import EmailCollector

__all__ = [
    "GitHubCollector",
    "LinkedInCollector",
    "TwitterCollector",
    "RedditCollector",
    "FacebookCollector",
    "InstagramCollector",
    "YouTubeCollector",
    "EmailCollector",
]