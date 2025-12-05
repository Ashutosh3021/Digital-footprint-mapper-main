"""
Instagram Collector Module

This module handles data collection from Instagram including:
- Public profile information
- Follower/following counts
- Bio and website information
"""

import requests
import asyncio
from typing import Dict, List, Any
from datetime import datetime
from bs4 import BeautifulSoup
import json
import re
from utils.rate_limiter import rate_limit

class InstagramCollector:
    def __init__(self):
        """Initialize Instagram collector"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
    async def collect_profile_data(self, username: str) -> Dict[str, Any]:
        """
        Collect public profile data from Instagram
        
        Args:
            username (str): Instagram username
            
        Returns:
            Dict containing profile data
        """
        await rate_limit("instagram")
        
        try:
            # Fetch profile page
            url = f"https://www.instagram.com/{username}/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract data from the page
            profile_data = {
                "username": username,
                "full_name": "",
                "bio": "",
                "website": "",
                "followers_count": 0,
                "following_count": 0,
                "posts_count": 0,
                "is_private": False,
                "is_verified": False
            }
            
            # Look for JSON data in script tags
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'window._sharedData' in script.string:
                    # Extract JSON data
                    json_str = script.string.replace('window._sharedData = ', '')[:-1]
                    try:
                        data = json.loads(json_str)
                        user_data = data.get('entry_data', {}).get('ProfilePage', [{}])[0].get('graphql', {}).get('user', {})
                        
                        if user_data:
                            profile_data.update({
                                "full_name": user_data.get('full_name', ''),
                                "bio": user_data.get('biography', ''),
                                "website": user_data.get('external_url', ''),
                                "followers_count": user_data.get('edge_followed_by', {}).get('count', 0),
                                "following_count": user_data.get('edge_follow', {}).get('count', 0),
                                "posts_count": user_data.get('edge_owner_to_timeline_media', {}).get('count', 0),
                                "is_private": user_data.get('is_private', False),
                                "is_verified": user_data.get('is_verified', False)
                            })
                            break
                    except:
                        pass
                        
            # If JSON extraction failed, try parsing from meta tags
            if not profile_data["full_name"]:
                # Get full name from title
                title = soup.find('title')
                if title:
                    title_text = title.get_text()
                    if title_text and 'on Instagram' in title_text:
                        profile_data["full_name"] = title_text.split('on Instagram')[0].strip()
                        
                # Get bio from meta description
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc:
                    desc_content = meta_desc.get('content', '')
                    # Extract bio (usually before the first parenthesis)
                    bio_match = re.search(r'^(.*?)\(', desc_content)
                    if bio_match:
                        profile_data["bio"] = bio_match.group(1).strip()
                        
            return profile_data
            
        except Exception as e:
            return {"error": f"Failed to collect Instagram data: {str(e)}"}
            
    async def collect_all_data(self, username: str) -> Dict[str, Any]:
        """
        Collect all available data from Instagram
        
        Args:
            username (str): Instagram username
            
        Returns:
            Dict containing all collected data
        """
        profile_data = await self.collect_profile_data(username)
        
        return {
            "platform": "Instagram",
            "profile": profile_data,
            "collected_at": datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    collector = InstagramCollector()
    
    # Example: Collect data for a profile
    # result = asyncio.run(collector.collect_all_data("example"))
    # print(result)
    pass