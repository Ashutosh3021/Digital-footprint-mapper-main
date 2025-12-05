"""
Facebook Collector Module

This module handles data collection from Facebook including:
- Public profile information extraction
- Friend count analysis
- Location data
"""

import requests
import asyncio
import re
from typing import Dict, List, Any
from datetime import datetime
from bs4 import BeautifulSoup
from utils.rate_limiter import rate_limit
from config import Config

class FacebookCollector:
    def __init__(self):
        """Initialize Facebook collector"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    async def collect_profile_data(self, profile_id: str) -> Dict[str, Any]:
        """
        Collect public profile data from Facebook
        
        Args:
            profile_id (str): Facebook profile ID or username
            
        Returns:
            Dict containing profile data
        """
        await rate_limit("facebook")
        
        try:
            # Construct profile URL
            if profile_id.isdigit():
                url = f"https://www.facebook.com/profile.php?id={profile_id}"
            else:
                url = f"https://www.facebook.com/{profile_id}"
                
            # Fetch profile page
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract profile information
            profile_data = {
                "name": "",
                "bio": "",
                "location": "",
                "work": "",
                "education": ""
            }
            
            # Try to extract name from title
            title = soup.find('title')
            if title:
                name = title.get_text().split('|')[0].strip()
                if name and "Facebook" not in name:
                    profile_data["name"] = name
                    
            # Look for bio information
            bio_elements = soup.find_all(['div', 'span'], class_=re.compile(r'bio|about', re.I))
            for element in bio_elements:
                text = element.get_text(strip=True)
                if text and len(text) > 20:  # Likely bio content
                    profile_data["bio"] = text[:500]  # Limit length
                    break
                    
            # Look for location information
            location_elements = soup.find_all(['div', 'span'], class_=re.compile(r'location|hometown', re.I))
            for element in location_elements:
                text = element.get_text(strip=True)
                if text and len(text) > 2 and len(text) < 50:
                    profile_data["location"] = text
                    break
                    
            return profile_data
            
        except Exception as e:
            return {"error": f"Failed to collect Facebook data: {str(e)}"}
            
    async def collect_all_data(self, profile_id: str) -> Dict[str, Any]:
        """
        Collect all available data from Facebook
        
        Args:
            profile_id (str): Facebook profile ID or username
            
        Returns:
            Dict containing all collected data
        """
        profile_data = await self.collect_profile_data(profile_id)
        
        return {
            "platform": "Facebook",
            "profile": profile_data,
            "collected_at": datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    collector = FacebookCollector()
    
    # Example: Collect data for a profile
    # result = asyncio.run(collector.collect_all_data("example"))
    # print(result)
    pass
