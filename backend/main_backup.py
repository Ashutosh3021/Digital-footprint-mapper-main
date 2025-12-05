from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional, List, Dict, Any
import asyncio
import json
from datetime import datetime
import networkx as nx
from pyvis.network import Network
import os
import re

# Import our custom modules
from collectors.github_collector import GitHubCollector
from collectors.linkedin_collector import LinkedInCollector
from collectors.twitter_collector import TwitterCollector
from collectors.reddit_collector import RedditCollector
from collectors.facebook_collector import FacebookCollector
from collectors.instagram_collector import InstagramCollector
from collectors.youtube_collector import YouTubeCollector
from collectors.email_collector import EmailCollector

# Import engines
from engines.data_fusion import data_fusion_engine
from engines.entity_resolution import entity_resolution_engine
from engines.risk_calculator import risk_calculator
from engines.tracker_detector import tracker_detector
from engines.visualization import visualization_engine

app = FastAPI(title="DFM OSINT Backend", description="Multi-Platform OSINT Collection and Analysis API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ScanInput(BaseModel):
    # Mandatory fields
    email: EmailStr
    github: str
    linkedin: HttpUrl
    # Optional fields
    twitter: Optional[str] = None
    reddit: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    youtube: Optional[str] = None

class PlatformLink(BaseModel):
    name: str
    handle: str
    url: str
    source: str  # "mandatory" | "optional" | "discovered"
    verified: bool

class Repository(BaseModel):
    name: str
    description: str
    url: str
    stars: int
    language: str
    last_updated: datetime

class DetailedFinding(BaseModel):
    platform: str
    type: str  # "exposed_secret" | "sensitive_info" | "suspicious_activity"
    description: str
    severity: str  # "critical" | "high" | "medium" | "low"
    evidence: str
    recommendation: str

class Tracker(BaseModel):
    name: str
    tracking_methods: List[str]
    confidence: float  # 0.0 - 1.0

class UsernamePrediction(BaseModel):
    platform: str
    predicted_username: str
    confidence: float

class ScanResult(BaseModel):
    scan_id: str
    email: str
    platforms: List[PlatformLink]
    profile_summary: Dict[str, Any]
    risk_score: Dict[str, Any]
    graph_data: Dict[str, Any]
    detailed_findings: List[DetailedFinding]
    trackers: List[Tracker]
    username_predictions: List[UsernamePrediction]
    created_at: datetime

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Main scan endpoint
@app.post("/api/v1/scan", response_model=ScanResult)
async def initiate_scan(scan_input: ScanInput):
    """Initiate a new OSINT scan"""
    scan_id = f"scan_{int(datetime.now().timestamp())}"
    
    try:
        # Initialize collectors
        github_collector = GitHubCollector()
        linkedin_collector = LinkedInCollector()
        email_collector = EmailCollector()
        
        # Initialize optional collectors if data provided
        twitter_collector = TwitterCollector() if scan_input.twitter else None
        reddit_collector = RedditCollector() if scan_input.reddit else None
        facebook_collector = FacebookCollector() if scan_input.facebook else None
        instagram_collector = InstagramCollector() if scan_input.instagram else None
        youtube_collector = YouTubeCollector() if scan_input.youtube else None
        
        # Collect data from platforms concurrently
        tasks = []
        
        # Mandatory collections
        tasks.append(github_collector.collect_all_data(scan_input.github))
        tasks.append(linkedin_collector.collect_all_data(str(scan_input.linkedin)))
        tasks.append(email_collector.collect_all_data(scan_input.email))
        
        # Optional collections
        if twitter_collector and scan_input.twitter:
            tasks.append(twitter_collector.collect_all_data(scan_input.twitter))
        if reddit_collector and scan_input.reddit:
            tasks.append(reddit_collector.collect_all_data(scan_input.reddit))
        if facebook_collector and scan_input.facebook:
            tasks.append(facebook_collector.collect_all_data(scan_input.facebook))
        if instagram_collector and scan_input.instagram:
            tasks.append(instagram_collector.collect_all_data(scan_input.instagram))
        if youtube_collector and scan_input.youtube:
            tasks.append(youtube_collector.collect_all_data(scan_input.youtube))
            
        # Execute all collection tasks
        platform_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and successful results
        successful_results = []
        for result in platform_results:
            if isinstance(result, Exception):
                # Log error but continue with successful results
                print(f"Collection error: {result}")
            else:
                successful_results.append(result)
                
        # Fuse data from all platforms
        unified_profile = data_fusion_engine.fuse_data(successful_results)
        
        # Perform entity resolution
        intelligence_graph = entity_resolution_engine.resolve_entities(unified_profile)
        
        # Calculate risk score
        risk_score = risk_calculator.calculate_risk_score(unified_profile, intelligence_graph)
        
        # Detect trackers
        trackers = tracker_detector.detect_trackers(unified_profile, intelligence_graph)
        
        # Generate graph visualization data
        graph_data = visualization_engine.export_graph_data(intelligence_graph)
        
        # Create detailed findings from collected data
        detailed_findings = []
        for result in successful_results:
            if isinstance(result, dict) and "repositories" in result:
                # Check for secrets in GitHub repositories
                repos = result.get("repositories", [])
                for repo in repos:
                    if repo.get("hasSecrets", False):
                        detailed_findings.append(DetailedFinding(
                            platform="GitHub",
                            type="exposed_secret",
                            description=f"Potential secrets found in repository {repo.get('name', 'unknown')}",
                            severity="high",
                            evidence=f"Repository contains {repo.get('secretCount', 0)} potential secrets",
                            recommendation="Remove exposed secrets and rotate any compromised credentials"
                        ))
        
        # Create username predictions based on patterns
        username_predictions = []
        identities = unified_profile.get("identities", {})
        if "github" in identities and "twitter" in identities:
            # Simple pattern prediction - if GitHub is john_doe_1990, Twitter might be johndoe1990
            github_username = identities["github"]
            # Remove underscores and keep alphanumeric
            predicted_twitter = re.sub(r'[^a-zA-Z0-9]', '', github_username)
            username_predictions.append(UsernamePrediction(
                platform="Twitter",
                predicted_username=predicted_twitter,
                confidence=0.7
            ))
        
        # Create platform links list
        platforms = []
        identities = unified_profile.get("identities", {})
        
        # Add mandatory platforms
        platforms.append(PlatformLink(
            name="GitHub",
            handle=identities.get("github", scan_input.github),
            url=f"https://github.com/{identities.get('github', scan_input.github)}",
            source="mandatory",
            verified=True
        ))
        
        platforms.append(PlatformLink(
            name="LinkedIn",
            handle=str(scan_input.linkedin),
            url=str(scan_input.linkedin),
            source="mandatory",
            verified=True
        ))
        
        platforms.append(PlatformLink(
            name="Email",
            handle=scan_input.email,
            url=f"mailto:{scan_input.email}",
            source="mandatory",
            verified=True
        ))
        
        # Add optional platforms
        if scan_input.twitter:
            platforms.append(PlatformLink(
                name="Twitter",
                handle=scan_input.twitter,
                url=f"https://twitter.com/{scan_input.twitter}",
                source="optional",
                verified=True
            ))
        if scan_input.reddit:
            platforms.append(PlatformLink(
                name="Reddit",
                handle=scan_input.reddit,
                url=f"https://reddit.com/user/{scan_input.reddit}",
                source="optional",
                verified=True
            ))
        if scan_input.facebook:
            platforms.append(PlatformLink(
                name="Facebook",
                handle=scan_input.facebook,
                url=f"https://facebook.com/{scan_input.facebook}",
                source="optional",
                verified=True
            ))
        if scan_input.instagram:
            platforms.append(PlatformLink(
                name="Instagram",
                handle=scan_input.instagram,
                url=f"https://instagram.com/{scan_input.instagram}",
                source="optional",
                verified=True
            ))
        if scan_input.youtube:
            platforms.append(PlatformLink(
                name="YouTube",
                handle=scan_input.youtube,
                url=f"https://youtube.com/{scan_input.youtube}",
                source="optional",
                verified=True
            ))
        
        # Create scan result
        scan_result = ScanResult(
            scan_id=scan_id,
            email=scan_input.email,
            platforms=platforms,
            profile_summary={
                "name": unified_profile.get("personal_info", {}).get("name", "Unknown"),
                "bio": unified_profile.get("personal_info", {}).get("bio", ""),
                "locations": unified_profile.get("locations", []),
                "organizations": unified_profile.get("organizations", [])
            },
            risk_score=risk_score,
            graph_data=graph_data,
            detailed_findings=detailed_findings,
            trackers=[Tracker(
                name=tracker["name"],
                tracking_methods=tracker["methods"],
                confidence=tracker["confidence"]
            ) for tracker in trackers],
            username_predictions=username_predictions,
            created_at=datetime.now()
        )
        
        # Cache the result for later retrieval
        import os
        import json
        
        # Create cache directory if it doesn't exist
        cache_dir = "scan_cache"
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        
        # Save result to cache file
        cache_file = os.path.join(cache_dir, f"{scan_id}.json")
        try:
            # Convert datetime to string for JSON serialization
            result_dict = scan_result.dict()
            result_dict["created_at"] = result_dict["created_at"].isoformat()
            with open(cache_file, 'w') as f:
                json.dump(result_dict, f)
        except Exception as cache_error:
            # Log error but don't fail the scan
            print(f"Warning: Failed to cache scan result: {cache_error}")
        
        return scan_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

# Get scan result endpoint
@app.get("/api/v1/scan/{scan_id}", response_model=ScanResult)
async def get_scan_result(scan_id: str):
    """Get the result of a previously initiated scan"""
    # In production, this would retrieve results from a database
    raise HTTPException(status_code=404, detail="Scan result not found")

# Breach check endpoint
@app.get("/api/v1/breach-check/{email}")
async def check_breaches(email: str):
    """Check if an email has been involved in known data breaches"""
    # This would query the HaveIBeenPwned API in production
    return {
        "email": email,
        "breaches_found": 0,
        "breaches": [],
        "checked_at": datetime.now().isoformat()
    }

# Graph visualization endpoint
@app.get("/api/v1/graph/visualize/{scan_id}")
async def visualize_graph(scan_id: str):
    """Get interactive graph visualization HTML"""
    # This would generate a visualization from stored data in production
    return {
        "scan_id": scan_id,
        "visualization_available": False,
        "message": "Graph visualization endpoint"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)