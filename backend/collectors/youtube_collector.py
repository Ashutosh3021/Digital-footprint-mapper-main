"""YouTube Collector Module

This module handles data collection from YouTube including:
- Channel statistics
- Subscriber count
- Video topics and upload frequency
- Channel description and metadata
"""

import requests
import asyncio
from typing import Dict, List, Any
from datetime import datetime
from utils.rate_limiter import rate_limit
from config import Config

class YouTubeCollector:
    def __init__(self, api_key: str = None):
        """Initialize YouTube collector
        
        Args:
            api_key (str, optional): YouTube Data API key
        """
        self.api_key = api_key or Config.YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
    async def collect_channel_data(self, channel_identifier: str) -> Dict[str, Any]:
        """
        Collect channel data from YouTube Data API
        
        Args:
            channel_identifier (str): YouTube channel ID or username
            
        Returns:
            Dict containing channel data
        """
        if not self.api_key:
            return {"error": "YouTube API key not configured"}
            
        await rate_limit("youtube")
        
        try:
            # First, resolve channel identifier to channel ID if needed
            channel_id = await self._resolve_channel_identifier(channel_identifier)
            if not channel_id:
                return {"error": "Could not resolve channel identifier"}
                
            # Fetch channel statistics
            params = {
                'part': 'snippet,statistics,brandingSettings',
                'id': channel_id,
                'key': self.api_key
            }
            
            response = requests.get(f"{self.base_url}/channels", params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'items' not in data or len(data['items']) == 0:
                return {"error": "Channel not found"}
                
            channel_data = data['items'][0]
            
            # Extract relevant information
            profile_data = {
                "channel_id": channel_data.get('id', ''),
                "title": channel_data.get('snippet', {}).get('title', ''),
                "description": channel_data.get('snippet', {}).get('description', ''),
                "published_at": channel_data.get('snippet', {}).get('publishedAt', ''),
                "thumbnails": channel_data.get('snippet', {}).get('thumbnails', {}),
                "view_count": int(channel_data.get('statistics', {}).get('viewCount', 0)),
                "subscriber_count": int(channel_data.get('statistics', {}).get('subscriberCount', 0)),
                "video_count": int(channel_data.get('statistics', {}).get('videoCount', 0)),
                "country": channel_data.get('snippet', {}).get('country', ''),
                "custom_url": channel_data.get('snippet', {}).get('customUrl', ''),
                "is_verified": False
            }
            
            # Check if channel is verified (in branding settings)
            branding = channel_data.get('brandingSettings', {})
            profile_data["is_verified"] = branding.get('channel', {}).get('verified', False)
            
            return profile_data
            
        except Exception as e:
            return {"error": f"Failed to collect YouTube data: {str(e)}"}
            
    async def _resolve_channel_identifier(self, identifier: str) -> str:
        """
        Resolve channel identifier (username or custom URL) to channel ID
        
        Args:
            identifier (str): Channel username, custom URL, or ID
            
        Returns:
            str: Channel ID
        """
        # If it looks like a channel ID already, return it
        if identifier.startswith('UC') and len(identifier) == 24:
            return identifier
            
        try:
            # Try to resolve as username
            params = {
                'part': 'id',
                'forUsername': identifier,
                'key': self.api_key
            }
            
            response = requests.get(f"{self.base_url}/channels", params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                return data['items'][0]['id']
                
        except:
            pass
            
        return None
        
    async def collect_recent_videos(self, channel_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Collect recent videos from a YouTube channel
        
        Args:
            channel_id (str): YouTube channel ID
            limit (int): Number of videos to fetch (max 50)
            
        Returns:
            List of recent videos
        """
        if not self.api_key:
            return [{"error": "YouTube API key not configured"}]
            
        await rate_limit("youtube")
        
        try:
            params = {
                'part': 'snippet,statistics,contentDetails',
                'channelId': channel_id,
                'maxResults': min(limit, 50),
                'order': 'date',
                'key': self.api_key
            }
            
            response = requests.get(f"{self.base_url}/search", params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'items' not in data:
                return []
                
            videos = []
            for item in data['items']:
                if item['id']['kind'] == 'youtube#video':
                    video_data = {
                        "video_id": item['id']['videoId'],
                        "title": item.get('snippet', {}).get('title', ''),
                        "description": item.get('snippet', {}).get('description', '')[:200],  # Limit length
                        "published_at": item.get('snippet', {}).get('publishedAt', ''),
                        "thumbnails": item.get('snippet', {}).get('thumbnails', {}),
                        "channel_id": item.get('snippet', {}).get('channelId', ''),
                        "channel_title": item.get('snippet', {}).get('channelTitle', '')
                    }
                    videos.append(video_data)
                    
            return videos
            
        except Exception as e:
            return [{"error": f"Failed to collect YouTube videos: {str(e)}"}]
            
    async def collect_all_data(self, channel_identifier: str) -> Dict[str, Any]:
        """
        Collect all available data from YouTube
        
        Args:
            channel_identifier (str): YouTube channel ID, username, or custom URL
            
        Returns:
            Dict containing all collected data
        """
        channel_data = await self.collect_channel_data(channel_identifier)
        channel_id = channel_data.get("channel_id")
        
        if channel_id:
            recent_videos = await self.collect_recent_videos(channel_id, 5)
        else:
            recent_videos = []
        
        return {
            "platform": "YouTube",
            "profile": channel_data,
            "recent_videos": recent_videos,
            "collected_at": datetime.now().isoformat()
        }