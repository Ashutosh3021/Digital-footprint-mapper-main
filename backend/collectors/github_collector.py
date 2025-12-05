"""
GitHub Collector Module

This module handles data collection from GitHub including:
- Profile metadata extraction
- Repository information gathering
- Secret detection in public repositories
"""

import requests
import re
import asyncio
from typing import Dict, List, Any
from datetime import datetime
from utils.rate_limiter import rate_limit
from config import Config

# Common secret patterns
SECRET_PATTERNS = Config.SECRET_PATTERNS

class GitHubCollector:
    def __init__(self, github_token: str = None):
        """
        Initialize GitHub collector
        
        Args:
            github_token (str, optional): GitHub personal access token for authenticated requests
        """
        self.github_token = github_token or Config.GITHUB_TOKEN
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'DFM-OSINT-Tool'
        }
        
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'
    
    async def collect_user_data(self, username: str) -> Dict[str, Any]:
        """
        Collect user profile data from GitHub
        
        Args:
            username (str): GitHub username
            
        Returns:
            Dict containing user profile data
        """
        try:
            # Rate limit to be ethical
            await rate_limit("github")
            
            # Get user profile
            user_url = f'https://api.github.com/users/{username}'
            user_response = requests.get(user_url, headers=self.headers, timeout=10)
            
            if user_response.status_code != 200:
                return {"error": f"Failed to fetch user data: {user_response.status_code}"}
            
            user_data = user_response.json()
            
            # Extract relevant information
            profile = {
                "name": user_data.get("name", ""),
                "bio": user_data.get("bio", ""),
                "location": user_data.get("location", ""),
                "company": user_data.get("company", ""),
                "website": user_data.get("blog", ""),
                "avatarUrl": user_data.get("avatar_url", ""),
                "followers": user_data.get("followers", 0),
                "following": user_data.get("following", 0),
                "public_repos": user_data.get("public_repos", 0),
                "created_at": user_data.get("created_at", ""),
                "updated_at": user_data.get("updated_at", "")
            }
            
            return profile
        except Exception as e:
            return {"error": f"Error collecting user data: {str(e)}"}
    
    async def collect_repositories(self, username: str) -> List[Dict[str, Any]]:
        """
        Collect user repositories from GitHub
        
        Args:
            username (str): GitHub username
            
        Returns:
            List of repository dictionaries
        """
        try:
            repos = []
            page = 1
            per_page = 100  # Max per page
            
            while True:
                # Rate limit to be ethical
                await rate_limit("github")
                
                repos_url = f'https://api.github.com/users/{username}/repos'
                params = {
                    'page': page,
                    'per_page': per_page,
                    'sort': 'updated',
                    'direction': 'desc'
                }
                
                repos_response = requests.get(repos_url, headers=self.headers, params=params, timeout=10)
                
                if repos_response.status_code != 200:
                    break
                
                page_repos = repos_response.json()
                
                if not page_repos:
                    break
                
                for repo in page_repos:
                    repo_info = {
                        "id": repo.get("id", ""),
                        "name": repo.get("name", ""),
                        "full_name": repo.get("full_name", ""),
                        "description": repo.get("description", ""),
                        "url": repo.get("html_url", ""),
                        "stars": repo.get("stargazers_count", 0),
                        "forks": repo.get("forks_count", 0),
                        "watchers": repo.get("watchers_count", 0),
                        "language": repo.get("language", ""),
                        "created_at": repo.get("created_at", ""),
                        "updated_at": repo.get("updated_at", ""),
                        "pushed_at": repo.get("pushed_at", ""),
                        "size": repo.get("size", 0),
                        "default_branch": repo.get("default_branch", ""),
                        "has_issues": repo.get("has_issues", False),
                        "has_projects": repo.get("has_projects", False),
                        "has_downloads": repo.get("has_downloads", False),
                        "has_wiki": repo.get("has_wiki", False),
                        "has_pages": repo.get("has_pages", False),
                        "archived": repo.get("archived", False),
                        "disabled": repo.get("disabled", False),
                        "open_issues": repo.get("open_issues", 0),
                        "license": repo.get("license", {}).get("name", "") if repo.get("license") else "",
                        "hasSecrets": False,
                        "secretCount": 0
                    }
                    
                    # Check for secrets in this repository
                    secrets = await self.check_repo_for_secrets(username, repo.get("name", ""))
                    if secrets and len(secrets) > 0:
                        repo_info["hasSecrets"] = True
                        repo_info["secretCount"] = len(secrets)
                    
                    repos.append(repo_info)
                
                # If we got less than per_page results, we're done
                if len(page_repos) < per_page:
                    break
                    
                page += 1
            
            return repos
        except Exception as e:
            return [{"error": f"Error collecting repositories: {str(e)}"}]
    
    async def check_repo_for_secrets(self, username: str, repo_name: str) -> List[Dict[str, Any]]:
        """
        Check a repository for exposed secrets in public code
        
        Args:
            username (str): GitHub username
            repo_name (str): Repository name
            
        Returns:
            List of found secrets
        """
        secrets = []
        
        try:
            # Search for secrets in code
            await rate_limit("github")
            
            search_url = f'https://api.github.com/search/code'
            params = {
                'q': f'user:{username} repo:{username}/{repo_name}',
                'per_page': 30  # Increased limit for better coverage
            }
            
            search_response = requests.get(search_url, headers=self.headers, params=params, timeout=10)
            
            if search_response.status_code == 200:
                search_results = search_response.json()
                items = search_results.get('items', [])
                
                # Check each file for secrets
                for item in items:
                    await rate_limit("github")
                    
                    file_url = item.get('url', '')
                    if file_url:
                        file_response = requests.get(file_url, headers=self.headers, timeout=10)
                        if file_response.status_code == 200:
                            file_data = file_response.json()
                            content = file_data.get('content', '')
                            
                            # Check for secrets in content
                            for pattern in SECRET_PATTERNS:
                                matches = re.findall(pattern, content, re.IGNORECASE)
                                for match in matches:
                                    secrets.append({
                                        "type": "potential_secret",
                                        "pattern": pattern[:30] + "..." if len(pattern) > 30 else pattern,
                                        "location": file_data.get("html_url", ""),
                                        "timestamp": datetime.now().isoformat()
                                    })
            
            return secrets
        except Exception as e:
            return [{"error": f"Error checking for secrets: {str(e)}"}]
    
    async def collect_all_data(self, username: str) -> Dict[str, Any]:
        """
        Collect all GitHub data for a user
        
        Args:
            username (str): GitHub username
            
        Returns:
            Dict containing all collected data
        """
        # Collect user profile
        profile = await self.collect_user_data(username)
        
        # Collect repositories
        repositories = await self.collect_repositories(username)
        
        # Compile results
        result = {
            "platform": "GitHub",
            "profile": profile,
            "repositories": repositories,
            "collected_at": datetime.now().isoformat()
        }
        
        return result

