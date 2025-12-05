"""
Twitter Collector Module

This module handles data collection from Twitter using Nitter (privacy-friendly frontend) including:
- Profile metadata extraction
- Follower/following counts
- Recent tweet analysis
"""

import requests
import asyncio
from typing import Dict, List, Any
from datetime import datetime
from bs4 import BeautifulSoup
from utils.rate_limiter import rate_limit

class TwitterCollector:
    def __init__(self):
        """Initialize Twitter collector using Nitter instances"""
        self.nitter_instances = [
            "https://nitter.net",
            "https://nitter.pussthecat.org",
            "https://nitter.privacydev.net"
        ]
        self.current_instance = 0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    async def collect_profile_data(self, username: str) -> Dict[str, Any]:
        """
        Collect profile data from Twitter via Nitter
        
        Args:
            username (str): Twitter username
            
        Returns:
            Dict containing profile data
        """
        await rate_limit("nitter")
        
        # Try different Nitter instances if one fails
        for i in range(len(self.nitter_instances)):
            instance = self.nitter_instances[self.current_instance]
            try:
                # Fetch profile page
                url = f"{instance}/{username}"
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    return self._parse_profile_data(soup, username)
                else:
                    # Try next instance
                    self.current_instance = (self.current_instance + 1) % len(self.nitter_instances)
                    
            except Exception as e:
                # Try next instance
                self.current_instance = (self.current_instance + 1) % len(self.nitter_instances)
                continue
                
        return {"error": "Failed to collect Twitter data from all Nitter instances"}
        
    def _parse_profile_data(self, soup: BeautifulSoup, username: str) -> Dict[str, Any]:
        """
        Parse profile data from Nitter HTML
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            username (str): Twitter username
            
        Returns:
            Dict containing parsed profile data
        """
        profile_data = {
            "username": username,
            "name": "",
            "bio": "",
            "location": "",
            "website": "",
            "join_date": "",
            "tweets_count": 0,
            "following_count": 0,
            "followers_count": 0,
            "likes_count": 0
        }
        
        try:
            # Extract profile name
            name_elem = soup.find('a', class_='profile-card-fullname')
            if name_elem:
                profile_data["name"] = name_elem.get_text(strip=True)
                
            # Extract bio
            bio_elem = soup.find('div', class_='profile-bio')
            if bio_elem:
                profile_data["bio"] = bio_elem.get_text(strip=True)
                
            # Extract location
            location_elem = soup.find('div', class_='profile-location')
            if location_elem:
                profile_data["location"] = location_elem.get_text(strip=True)
                
            # Extract website
            website_elem = soup.find('div', class_='profile-website')
            if website_elem:
                link = website_elem.find('a')
                if link:
                    profile_data["website"] = link.get('href', '')
                    
            # Extract join date
            join_elem = soup.find('div', class_='profile-joindate')
            if join_elem:
                profile_data["join_date"] = join_elem.get_text(strip=True)
                
            # Extract stats
            stats_elems = soup.find_all('span', class_='profile-stat-num')
            if len(stats_elems) >= 4:
                try:
                    profile_data["tweets_count"] = int(stats_elems[0].get_text(strip=True).replace(',', ''))
                    profile_data["following_count"] = int(stats_elems[1].get_text(strip=True).replace(',', ''))
                    profile_data["followers_count"] = int(stats_elems[2].get_text(strip=True).replace(',', ''))
                    profile_data["likes_count"] = int(stats_elems[3].get_text(strip=True).replace(',', ''))
                except ValueError:
                    pass  # Keep default values if parsing fails
                    
        except Exception as e:
            profile_data["parsing_error"] = str(e)
            
        return profile_data
        
    async def collect_recent_tweets(self, username: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Collect recent tweets from a Twitter user via Nitter
        
        Args:
            username (str): Twitter username
            limit (int): Number of tweets to fetch
            
        Returns:
            List of recent tweets
        """
        await rate_limit("nitter")
        
        tweets = []
        
        # Try different Nitter instances if one fails
        for i in range(len(self.nitter_instances)):
            instance = self.nitter_instances[self.current_instance]
            try:
                # Fetch tweets page
                url = f"{instance}/{username}"
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    tweets = self._parse_recent_tweets(soup, limit)
                    break
                else:
                    # Try next instance
                    self.current_instance = (self.current_instance + 1) % len(self.nitter_instances)
                    
            except Exception as e:
                # Try next instance
                self.current_instance = (self.current_instance + 1) % len(self.nitter_instances)
                continue
                
        return tweets
        
    def _parse_recent_tweets(self, soup: BeautifulSoup, limit: int) -> List[Dict[str, Any]]:
        """
        Parse recent tweets from Nitter HTML
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            limit (int): Number of tweets to parse
            
        Returns:
            List of parsed tweets
        """
        tweets = []
        tweet_elements = soup.find_all('div', class_='timeline-item')
        
        for tweet_elem in tweet_elements[:limit]:
            try:
                tweet_data = {
                    "text": "",
                    "date": "",
                    "retweets": 0,
                    "quotes": 0,
                    "comments": 0,
                    "likes": 0
                }
                
                # Extract tweet text
                content_elem = tweet_elem.find('div', class_='tweet-content')
                if content_elem:
                    tweet_data["text"] = content_elem.get_text(strip=True)[:280]  # Limit to tweet length
                    
                # Extract date
                date_elem = tweet_elem.find('span', class_='tweet-date')
                if date_elem:
                    tweet_data["date"] = date_elem.get_text(strip=True)
                    
                # Extract engagement metrics
                stats_elem = tweet_elem.find('div', class_='tweet-stats')
                if stats_elem:
                    # Parse individual stats
                    stat_items = stats_elem.find_all('span', class_='tweet-stat')
                    for stat_item in stat_items:
                        stat_text = stat_item.get_text(strip=True)
                        if 'retweet' in stat_text.lower():
                            try:
                                tweet_data["retweets"] = int(stat_text.split()[0])
                            except:
                                pass
                        elif 'quote' in stat_text.lower():
                            try:
                                tweet_data["quotes"] = int(stat_text.split()[0])
                            except:
                                pass
                        elif 'comment' in stat_text.lower():
                            try:
                                tweet_data["comments"] = int(stat_text.split()[0])
                            except:
                                pass
                        elif 'like' in stat_text.lower():
                            try:
                                tweet_data["likes"] = int(stat_text.split()[0])
                            except:
                                pass
                                
                tweets.append(tweet_data)
                
            except Exception as e:
                # Skip malformed tweets
                continue
                
        return tweets
        
    async def collect_all_data(self, username: str) -> Dict[str, Any]:
        """
        Collect all available data from Twitter via Nitter
        
        Args:
            username (str): Twitter username
            
        Returns:
            Dict containing all collected data
        """
        profile_data = await self.collect_profile_data(username)
        recent_tweets = await self.collect_recent_tweets(username, 5)
        
        return {
            "platform": "Twitter",
            "profile": profile_data,
            "recent_tweets": recent_tweets,
            "collected_at": datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    collector = TwitterCollector()
    
    # Example: Collect data for a user
    # result = asyncio.run(collector.collect_all_data("example"))
    # print(result)
    pass