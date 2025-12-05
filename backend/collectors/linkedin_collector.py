"""
LinkedIn Collector Module

This module handles data collection from LinkedIn including:
- Profile metadata extraction
- Company affiliation gathering
- Professional connections analysis
"""

import requests
import asyncio
from typing import Dict, List, Any
from datetime import datetime
from bs4 import BeautifulSoup
from utils.rate_limiter import rate_limit
from config import Config

class LinkedInCollector:
    def __init__(self, api_key: str = None):
        """
        Initialize LinkedIn collector
        
        Args:
            api_key (str, optional): Clearbit API key for enhanced data collection
        """
        self.clearbit_api_key = api_key or Config.CLEARBIT_API_KEY
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    async def collect_profile_data(self, profile_url: str) -> Dict[str, Any]:
        """
        Collect profile data from LinkedIn
        
        Args:
            profile_url (str): LinkedIn profile URL
            
        Returns:
            Dict containing profile data
        """
        await rate_limit("linkedin")
        
        try:
            # Scrape public LinkedIn profile
            response = requests.get(profile_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract basic profile information
            profile_data = {
                "name": "",
                "headline": "",
                "location": "",
                "connections": "",
                "about": ""
            }
            
            # Get name
            name_element = soup.find('h1', class_='top-card-layout__title')
            if name_element:
                profile_data["name"] = name_element.get_text(strip=True)
                
            # Get headline
            headline_element = soup.find('h2', class_='top-card-layout__headline')
            if headline_element:
                profile_data["headline"] = headline_element.get_text(strip=True)
                
            # Get location
            location_element = soup.find('span', class_='top-card__subline-item')
            if location_element:
                profile_data["location"] = location_element.get_text(strip=True)
                
            # Get connections count
            connections_element = soup.find('span', class_='top-card__subline-item-link')
            if connections_element:
                profile_data["connections"] = connections_element.get_text(strip=True)
                
            # Get about section
            about_element = soup.find('p', class_='summary__blurb')
            if about_element:
                profile_data["about"] = about_element.get_text(strip=True)
                
            # Use Clearbit API for enhanced data if available
            if self.clearbit_api_key and profile_data["name"]:
                clearbit_data = await self._get_clearbit_data(profile_data["name"])
                profile_data.update(clearbit_data)
                
            return profile_data
            
        except Exception as e:
            return {"error": f"Failed to collect LinkedIn data: {str(e)}"}
            
    async def _get_clearbit_data(self, name: str) -> Dict[str, Any]:
        """
        Get enhanced profile data from Clearbit API
        
        Args:
            name (str): Person's name
            
        Returns:
            Dict containing enhanced profile data
        """
        if not self.clearbit_api_key:
            return {}
            
        try:
            await rate_limit("clearbit")
            
            # Clearbit person lookup
            url = f"https://person.clearbit.com/v2/people/find?name={name}"
            headers = {
                "Authorization": f"Bearer {self.clearbit_api_key}",
                "User-Agent": "DFM-OSINT-Tool"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            clearbit_data = {
                "company": "",
                "role": "",
                "verified": False
            }
            
            if "company" in data and data["company"]:
                clearbit_data["company"] = data["company"].get("name", "")
                clearbit_data["role"] = data.get("employment", {}).get("title", "")
                clearbit_data["verified"] = True
                
            return clearbit_data
            
        except Exception as e:
            return {"clearbit_error": str(e)}
            
    async def collect_all_data(self, profile_url: str) -> Dict[str, Any]:
        """
        Collect all available data from LinkedIn
        
        Args:
            profile_url (str): LinkedIn profile URL
            
        Returns:
            Dict containing all collected data
        """
        profile_data = await self.collect_profile_data(profile_url)
        
        return {
            "platform": "LinkedIn",
            "profile": profile_data,
            "collected_at": datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    # This would typically be run with a valid API key
    collector = LinkedInCollector()
    
    # Example: Collect data for a profile
    # result = asyncio.run(collector.collect_all_data("https://linkedin.com/in/testuser"))
    # print(result)
    pass