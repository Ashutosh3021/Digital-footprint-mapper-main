"""Tracker Detector Engine

This module identifies potential surveillance entities based on platform usage
and other indicators.
"""

from typing import Dict, List, Any
import networkx as nx

class TrackerDetector:
    def __init__(self):
        """Initialize the tracker detector with known tracker rules"""
        self.tracker_rules = {
            "google": {
                "platforms": ["gmail", "youtube", "google+"],
                "confidence": 0.9,
                "methods": ["Analytics", "Gmail metadata", "YouTube tracking"]
            },
            "microsoft": {
                "platforms": ["linkedin", "outlook"],
                "confidence": 0.8,
                "methods": ["Insight Tag", "profile scraping"]
            },
            "x_corp": {
                "platforms": ["twitter", "x"],
                "confidence": 0.7,
                "methods": ["ad targeting", "behavioral profiling"]
            },
            "facebook": {
                "platforms": ["facebook", "instagram", "whatsapp"],
                "confidence": 0.85,
                "methods": ["cross-platform tracking", "behavioral profiling"]
            },
            "data_brokers": {
                "platforms": [],  # Detected via breach checks
                "confidence": 0.6,
                "methods": ["aggregation services", "data brokerage"]
            }
        }
        
    def detect_trackers(self, unified_profile: Dict[str, Any], 
                       intelligence_graph: nx.Graph) -> List[Dict[str, Any]]:
        """
        Detect potential trackers based on platform usage and other indicators
        
        Args:
            unified_profile (Dict): Unified user profile
            intelligence_graph (nx.Graph): Intelligence graph
            
        Returns:
            List[Dict]: List of detected trackers
        """
        trackers = []
        identities = unified_profile.get("identities", {})
        platforms = set(identities.keys())
        
        # Check each tracker rule
        for tracker_name, rule in self.tracker_rules.items():
            matched_platforms = platforms.intersection(set(rule["platforms"]))
            
            if matched_platforms:
                # Calculate confidence based on number of matched platforms
                base_confidence = rule["confidence"]
                confidence_boost = len(matched_platforms) * 0.05
                final_confidence = min(base_confidence + confidence_boost, 1.0)
                
                trackers.append({
                    "name": tracker_name,
                    "matched_platforms": list(matched_platforms),
                    "methods": rule["methods"],
                    "confidence": round(final_confidence, 2),
                    "detected_at": "profile_analysis"
                })
                
        # Check for data broker tracking based on email exposure
        emails = unified_profile.get("emails", [])
        if emails:
            # If email found in breaches (this would come from HIBP integration)
            # For now, we'll add a general data broker tracker
            trackers.append({
                "name": "data_brokers",
                "matched_platforms": [],
                "methods": ["email harvesting", "data aggregation"],
                "confidence": 0.6,
                "detected_at": "email_exposure"
            })
            
        return trackers

# Create a singleton instance
tracker_detector = TrackerDetector()