"""Data Fusion Engine

This module handles the normalization of data from disparate platform formats
into a unified user profile structure.
"""

import networkx as nx
from typing import Dict, List, Any, Set
from datetime import datetime
import re

class DataFusionEngine:
    def __init__(self):
        """Initialize the data fusion engine"""
        pass
        
    def fuse_data(self, platform_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Fuse data from multiple platforms into a unified profile
        
        Args:
            platform_data (List[Dict]): List of data from different platforms
            
        Returns:
            Dict containing unified profile data
        """
        # Initialize unified profile
        unified_profile = {
            "identities": {},
            "personal_info": {},
            "professional_info": {},
            "social_metrics": {},
            "locations": set(),
            "websites": set(),
            "organizations": set(),
            "emails": set(),
            "phones": set(),
            "collected_at": datetime.now().isoformat()
        }
        
        # Process data from each platform
        for data in platform_data:
            platform = data.get("platform", "unknown")
            if platform == "GitHub":
                self._fuse_github_data(unified_profile, data)
            elif platform == "LinkedIn":
                self._fuse_linkedin_data(unified_profile, data)
            elif platform == "Twitter":
                self._fuse_twitter_data(unified_profile, data)
            elif platform == "Reddit":
                self._fuse_reddit_data(unified_profile, data)
            elif platform == "Facebook":
                self._fuse_facebook_data(unified_profile, data)
            elif platform == "Instagram":
                self._fuse_instagram_data(unified_profile, data)
            elif platform == "YouTube":
                self._fuse_youtube_data(unified_profile, data)
            elif platform == "Email":
                self._fuse_email_data(unified_profile, data)
                
        # Convert sets to lists for JSON serialization
        unified_profile["locations"] = list(unified_profile["locations"])
        unified_profile["websites"] = list(unified_profile["websites"])
        unified_profile["organizations"] = list(unified_profile["organizations"])
        unified_profile["emails"] = list(unified_profile["emails"])
        unified_profile["phones"] = list(unified_profile["phones"])
        
        return unified_profile
        
    def _fuse_github_data(self, profile: Dict[str, Any], data: Dict[str, Any]):
        """Fuse GitHub data into unified profile"""
        profile_data = data.get("profile", {})
        
        # Add GitHub identity
        if profile_data.get("login"):
            profile["identities"]["github"] = profile_data["login"]
            
        # Extract personal info
        if profile_data.get("name"):
            profile["personal_info"]["name"] = profile_data["name"]
        if profile_data.get("email"):
            profile["emails"].add(profile_data["email"])
            profile["identities"]["email"] = profile_data["email"]
        if profile_data.get("bio"):
            profile["personal_info"]["bio"] = profile_data["bio"]
        if profile_data.get("location"):
            profile["locations"].add(profile_data["location"])
        if profile_data.get("blog"):
            profile["websites"].add(profile_data["blog"])
            
        # Extract professional info
        if profile_data.get("company"):
            profile["organizations"].add(profile_data["company"])
            
        # Extract social metrics
        profile["social_metrics"]["github_followers"] = profile_data.get("followers", 0)
        profile["social_metrics"]["github_public_repos"] = profile_data.get("public_repos", 0)
        
    def _fuse_linkedin_data(self, profile: Dict[str, Any], data: Dict[str, Any]):
        """Fuse LinkedIn data into unified profile"""
        profile_data = data.get("profile", {})
        
        # Extract personal info
        if profile_data.get("name"):
            profile["personal_info"]["name"] = profile_data["name"]
        if profile_data.get("headline"):
            profile["professional_info"]["headline"] = profile_data["headline"]
        if profile_data.get("location"):
            profile["locations"].add(profile_data["location"])
        if profile_data.get("about"):
            profile["personal_info"]["bio"] = profile_data["about"]
            
        # Extract professional info
        if profile_data.get("company"):
            profile["organizations"].add(profile_data["company"])
        if profile_data.get("role"):
            profile["professional_info"]["role"] = profile_data["role"]
            
    def _fuse_twitter_data(self, profile: Dict[str, Any], data: Dict[str, Any]):
        """Fuse Twitter data into unified profile"""
        profile_data = data.get("profile", {})
        
        # Add Twitter identity
        if profile_data.get("username"):
            profile["identities"]["twitter"] = profile_data["username"]
            
        # Extract personal info
        if profile_data.get("name"):
            profile["personal_info"]["name"] = profile_data["name"]
        if profile_data.get("bio"):
            profile["personal_info"]["bio"] = profile_data["bio"]
        if profile_data.get("location"):
            profile["locations"].add(profile_data["location"])
        if profile_data.get("website"):
            profile["websites"].add(profile_data["website"])
            
        # Extract social metrics
        profile["social_metrics"]["twitter_followers"] = profile_data.get("followers_count", 0)
        profile["social_metrics"]["twitter_following"] = profile_data.get("following_count", 0)
        profile["social_metrics"]["twitter_tweets"] = profile_data.get("tweets_count", 0)
        
    def _fuse_reddit_data(self, profile: Dict[str, Any], data: Dict[str, Any]):
        """Fuse Reddit data into unified profile"""
        profile_data = data.get("profile", {})
        
        # Add Reddit identity
        if profile_data.get("name"):
            profile["identities"]["reddit"] = profile_data["name"]
            
        # Extract social metrics
        profile["social_metrics"]["reddit_link_karma"] = profile_data.get("link_karma", 0)
        profile["social_metrics"]["reddit_comment_karma"] = profile_data.get("comment_karma", 0)
        
        # Check for email in profile (rare but possible)
        if profile_data.get("has_verified_email"):
            # We don't have the actual email, but we know it's verified
            pass
            
    def _fuse_facebook_data(self, profile: Dict[str, Any], data: Dict[str, Any]):
        """Fuse Facebook data into unified profile"""
        profile_data = data.get("profile", {})
        
        # Extract personal info
        if profile_data.get("name"):
            profile["personal_info"]["name"] = profile_data["name"]
        if profile_data.get("bio"):
            profile["personal_info"]["bio"] = profile_data["bio"]
        if profile_data.get("location"):
            profile["locations"].add(profile_data["location"])
            
    def _fuse_instagram_data(self, profile: Dict[str, Any], data: Dict[str, Any]):
        """Fuse Instagram data into unified profile"""
        profile_data = data.get("profile", {})
        
        # Add Instagram identity
        if data.get("username"):
            profile["identities"]["instagram"] = data["username"]
            
        # Extract personal info
        if profile_data.get("full_name"):
            profile["personal_info"]["name"] = profile_data["full_name"]
        if profile_data.get("bio"):
            profile["personal_info"]["bio"] = profile_data["bio"]
        if profile_data.get("website"):
            profile["websites"].add(profile_data["website"])
            
        # Extract social metrics
        profile["social_metrics"]["instagram_followers"] = profile_data.get("followers_count", 0)
        profile["social_metrics"]["instagram_following"] = profile_data.get("following_count", 0)
        profile["social_metrics"]["instagram_posts"] = profile_data.get("posts_count", 0)
        
    def _fuse_youtube_data(self, profile: Dict[str, Any], data: Dict[str, Any]):
        """Fuse YouTube data into unified profile"""
        profile_data = data.get("profile", {})
        
        # Extract personal info
        if profile_data.get("title"):
            profile["personal_info"]["name"] = profile_data["title"]
        if profile_data.get("description"):
            profile["personal_info"]["bio"] = profile_data["description"]
            
        # Extract social metrics
        profile["social_metrics"]["youtube_subscribers"] = profile_data.get("subscriber_count", 0)
        profile["social_metrics"]["youtube_views"] = profile_data.get("view_count", 0)
        profile["social_metrics"]["youtube_videos"] = profile_data.get("video_count", 0)
        
    def _fuse_email_data(self, profile: Dict[str, Any], data: Dict[str, Any]):
        """Fuse email data into unified profile"""
        email_data = data.get("data", {})
        
        # Add email identity
        if email_data.get("email"):
            profile["identities"]["email"] = email_data["email"]
            profile["emails"].add(email_data["email"])
            
        # Extract domain as organization if corporate
        if email_data.get("corporate") and email_data.get("domain"):
            profile["organizations"].add(email_data["domain"])

# Create a singleton instance
data_fusion_engine = DataFusionEngine()