"""
Reddit Collector Module

This module handles data collection from Reddit including:
- User profile information
- Karma scores
- Account age
- Post history analysis
"""

import requests
import asyncio
from typing import Dict, List, Any
from datetime import datetime
from utils.rate_limiter import rate_limit

class RedditCollector:
    def __init__(self):
        """Initialize Reddit collector"""
        self.base_url = "https://www.reddit.com"
        self.headers = {
            'User-Agent': 'DFM-OSINT-Tool/1.0 (by /u/dfm-osint)'
        }
        
    async def collect_user_data(self, username: str) -> Dict[str, Any]:
        """
        Collect user data from Reddit API
        
        Args:
            username (str): Reddit username
            
        Returns:
            Dict containing user data
        """
        await rate_limit("reddit")
        
        try:
            # Fetch user about data
            about_url = f"{self.base_url}/user/{username}/about.json"
            response = requests.get(about_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if "data" not in data:
                return {"error": "User not found or data unavailable"}
                
            user_data = data["data"]
            
            # Extract relevant information
            profile_data = {
                "name": user_data.get("name", ""),
                "created_utc": user_data.get("created_utc", 0),
                "link_karma": user_data.get("link_karma", 0),
                "comment_karma": user_data.get("comment_karma", 0),
                "is_gold": user_data.get("is_gold", False),
                "is_mod": user_data.get("is_mod", False),
                "verified": user_data.get("verified", False),
                "has_verified_email": user_data.get("has_verified_email", False)
            }
            
            # Calculate account age
            if profile_data["created_utc"] > 0:
                created_date = datetime.fromtimestamp(profile_data["created_utc"])
                profile_data["account_age_days"] = (datetime.now() - created_date).days
                
            return profile_data
            
        except Exception as e:
            return {"error": f"Failed to collect Reddit data: {str(e)}"}
            
    async def collect_recent_posts(self, username: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Collect recent posts from a Reddit user
        
        Args:
            username (str): Reddit username
            limit (int): Number of posts to fetch (max 100)
            
        Returns:
            List of recent posts
        """
        await rate_limit("reddit")
        
        try:
            # Fetch user overview (posts and comments)
            overview_url = f"{self.base_url}/user/{username}/overview.json?limit={limit}"
            response = requests.get(overview_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if "data" not in data or "children" not in data["data"]:
                return []
                
            posts = []
            for item in data["data"]["children"]:
                if item["kind"] == "t3":  # Posts only (not comments)
                    post_data = item["data"]
                    posts.append({
                        "title": post_data.get("title", ""),
                        "subreddit": post_data.get("subreddit", ""),
                        "score": post_data.get("score", 0),
                        "created_utc": post_data.get("created_utc", 0),
                        "url": post_data.get("url", ""),
                        "selftext": post_data.get("selftext", "")[:200]  # Limit length
                    })
                    
            return posts
            
        except Exception as e:
            return [{"error": f"Failed to collect Reddit posts: {str(e)}"}]
            
    async def collect_all_data(self, username: str) -> Dict[str, Any]:
        """
        Collect all available data from Reddit
        
        Args:
            username (str): Reddit username
            
        Returns:
            Dict containing all collected data
        """
        user_data = await self.collect_user_data(username)
        recent_posts = await self.collect_recent_posts(username, 5)
        
        return {
            "platform": "Reddit",
            "profile": user_data,
            "recent_posts": recent_posts,
            "collected_at": datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    collector = RedditCollector()
    
    # Example: Collect data for a user
    # result = asyncio.run(collector.collect_all_data("example"))
    # print(result)
    pass