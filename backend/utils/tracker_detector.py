"""Tracker Detection Utility

This module provides functionality to detect potential tracking entities
based on platform usage and other indicators.
"""

from typing import List, Dict, Any

# Default configuration for standalone use
class Config:
    TRACKER_RULES = {
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
        "data_brokers": {
            "platforms": [],  # Detected via breach checks
            "confidence": 0.85,
            "methods": ["aggregation", "profiling", "selling data"]
        }
    }

class TrackerDetector:
    def __init__(self, config: Config = None):
        """
        Initialize tracker detector
        
        Args:
            config (Config): Configuration object with tracker rules
        """
        self.config = config or Config()
        self.tracker_rules = self.config.TRACKER_RULES
    
    def detect_trackers(self, platforms: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect potential trackers based on platform usage
        
        Args:
            platforms (List[Dict]): List of platform information
            
        Returns:
            List of detected trackers
        """
        trackers = []
        platform_names = [p.get("name", "").lower() for p in platforms]
        
        for tracker_name, rule in self.tracker_rules.items():
            matched_platforms = []
            for platform in rule["platforms"]:
                if platform.lower() in platform_names:
                    matched_platforms.append(platform)
            
            if matched_platforms:
                # Calculate confidence based on number of matched platforms
                base_confidence = rule["confidence"]
                confidence_boost = len(matched_platforms) * 0.05
                final_confidence = min(base_confidence + confidence_boost, 1.0)
                
                trackers.append({
                    "name": tracker_name,
                    "platforms": matched_platforms,
                    "methods": rule["methods"],
                    "confidence": round(final_confidence, 2)
                })
        
        return trackers

# Global tracker detector instance
tracker_detector = TrackerDetector()

# Convenience functions
def detect_trackers(platforms: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Detect trackers based on platform usage"""
    return tracker_detector.detect_trackers(platforms)

def calculate_tracker_risk(trackers: List[Dict[str, Any]]) -> float:
    """Calculate overall tracker risk score"""
    if not trackers:
        return 0.0
    
    total_confidence = sum(t.get("confidence", 0) for t in trackers)
    return min(total_confidence / len(trackers) * 100, 100)