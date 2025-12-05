from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import json

Base = declarative_base()

class ScanSession(Base):
    __tablename__ = 'scan_sessions'
    
    id = Column(Integer, primary_key=True)
    scan_id = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    email = Column(String(255), nullable=False)
    github_username = Column(String(100), nullable=False)
    linkedin_url = Column(Text, nullable=False)
    twitter_handle = Column(String(100))
    reddit_username = Column(String(100))
    facebook_id = Column(String(100))
    instagram_handle = Column(String(100))
    youtube_channel = Column(String(100))
    
    # Relationships
    results = relationship("ScanResult", back_populates="session", uselist=False)
    platforms = relationship("PlatformLink", back_populates="session")
    repositories = relationship("Repository", back_populates="session")
    findings = relationship("Finding", back_populates="session")
    breaches = relationship("Breach", back_populates="session")
    trackers = relationship("Tracker", back_populates="session")

class ScanResult(Base):
    __tablename__ = 'scan_results'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('scan_sessions.id'))
    username = Column(String(100), nullable=False)
    profile_data = Column(Text)  # JSON string
    emails = Column(Text)  # JSON array string
    organizations = Column(Text)  # JSON array string
    risk_score_overall = Column(Integer)
    risk_score_sensitivity = Column(Integer)
    risk_score_cross_platform = Column(Integer)
    risk_score_recency = Column(Integer)
    risk_score_exploitability = Column(Integer)
    risk_score_insight = Column(Text)
    
    # Relationships
    session = relationship("ScanSession", back_populates="results")

class PlatformLink(Base):
    __tablename__ = 'platform_links'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('scan_sessions.id'))
    name = Column(String(50), nullable=False)
    handle = Column(String(100), nullable=False)
    url = Column(Text, nullable=False)
    source = Column(String(20), nullable=False)  # "mandatory", "optional", "discovered"
    verified = Column(Integer, default=0)  # 0 or 1 for boolean
    
    # Relationships
    session = relationship("ScanSession", back_populates="platforms")

class Repository(Base):
    __tablename__ = 'repositories'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('scan_sessions.id'))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    url = Column(Text, nullable=False)
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    last_updated = Column(String(20))  # Date string
    has_secrets = Column(Integer, default=0)  # 0 or 1 for boolean
    secret_count = Column(Integer, default=0)
    
    # Relationships
    session = relationship("ScanSession", back_populates="repositories")

class Finding(Base):
    __tablename__ = 'findings'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('scan_sessions.id'))
    type = Column(String(50), nullable=False)
    severity = Column(String(10), nullable=False)  # "critical", "high", "medium", "low"
    description = Column(Text, nullable=False)
    location = Column(Text)
    url = Column(Text)
    
    # Relationships
    session = relationship("ScanSession", back_populates="findings")

class Breach(Base):
    __tablename__ = 'breaches'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('scan_sessions.id'))
    name = Column(String(100), nullable=False)
    date = Column(String(20), nullable=False)  # Date string
    email = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(String(10), nullable=False)  # "critical", "high", "medium", "low"
    data_types = Column(Text)  # JSON array string
    
    # Relationships
    session = relationship("ScanSession", back_populates="breaches")

class Tracker(Base):
    __tablename__ = 'trackers'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('scan_sessions.id'))
    name = Column(String(100), nullable=False)
    methods = Column(Text)  # JSON array string
    confidence = Column(Integer)  # 0-100 as integer
    explanation = Column(Text)
    url = Column(Text)
    
    # Relationships
    session = relationship("ScanSession", back_populates="trackers")

# Patterns table for username prediction
class UsernamePattern(Base):
    __tablename__ = 'username_patterns'
    
    id = Column(Integer, primary_key=True)
    pattern_key = Column(String(50), unique=True, nullable=False)  # e.g., "github_to_twitter"
    pattern_value = Column(String(100), nullable=False)  # e.g., "remove_underscores"
    created_at = Column(DateTime, default=datetime.utcnow)
    usage_count = Column(Integer, default=1)