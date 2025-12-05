"""
Configuration Module

This module contains configuration settings for the DFM OSINT backend.
"""

import os
from typing import List

class Config:
    # API Keys (should be loaded from environment variables in production)
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    CLEARBIT_API_KEY = os.getenv("CLEARBIT_API_KEY", "")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./osint_data.db")
    
    # Rate Limiting Settings
    REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", "1.0"))  # Seconds between requests
    MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "5"))
    
    # Secret Detection Patterns
    SECRET_PATTERNS: List[str] = [
        r'(?i)api[_\s]?key[\"\s]*[=:][\"\s]*[a-z0-9]{32,}',
        r'(?i)password[\"\s]*[=:][\"\s]*[^\s]+',
        r'(?i)secret[\"\s]*[=:][\"\s]*[a-z0-9]{32,}',
        r'(?i)token[\"\s]*[=:][\"\s]*[a-z0-9]{20,}',
        r'(?i)aws[_\s]?access[_\s]?key[\"\s]*[=:][\"\s]*[A-Z0-9]{20}',
        r'(?i)aws[_\s]?secret[_\s]?key[\"\s]*[=:][\"\s]*[A-Za-z0-9/+=]{40}',
        r'(?i)github[_\s]?token[\"\s]*[=:][\"\s]*[a-zA-Z0-9_]{35,40}',
        r'(?i)slack[_\s]?token[\"\s]*[=:][\"\s]*[a-z0-9\-]{32,}',
        r'(?i)firebase[\"\s]*[=:][\"\s]*[a-z0-9\-]{30,}',
        r'(?i)heroku[\"\s]*[=:][\"\s]*[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}',
        r'(?i)stripe[_\s]?sk[_\s]?live[\"\s]*[=:][\"\s]*[a-zA-Z0-9]{24,}',
        r'(?i)twilio[_\s]?auth[_\s]?token[\"\s]*[=:][\"\s]*[a-z0-9]{32}',
        r'(?i)sendgrid[_\s]?api[_\s]?key[\"\s]*[=:][\"\s]*[A-Za-z0-9\-_]{30,}',
        r'(?i)mailgun[_\s]?api[_\s]?key[\"\s]*[=:][\"\s]*[a-z0-9]{32}',
        r'(?i)paypal[_\s]?client[_\s]?id[\"\s]*[=:][\"\s]*[a-zA-Z0-9]{16,}'
    ]
    
    # Tracker Detection Rules
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
    
    # Risk Calculation Weights
    RISK_WEIGHTS = {
        "data_sensitivity": 0.4,
        "cross_platform": 0.25,
        "recency": 0.2,
        "exploitability": 0.15
    }