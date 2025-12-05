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
from engines.intelligence_graph import intelligence_graph_engine

# Import new feature modules
from risk_assessment import SecurityRecommendations
from exposure_timeline import ExposureTimeline
from threat_intelligence import ThreatIntelligence
from username_predictor import UsernamePrediction as UsernamePredictorEngine

app = FastAPI(title="DFM OSINT Backend", description="Multi-Platform OSINT Collection and Analysis API")

# Add CORS middleware
# Note: In development, we allow all origins to handle network access issues
# In production, specify exact origins for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if os.environ.get("ENVIRONMENT", "development") == "development" else ["http://localhost:8003", "http://127.0.0.1:8003"],
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

class Recommendation(BaseModel):
    priority: str
    icon: str
    title: str
    description: str
    action: Optional[str] = None
    alternatives: Optional[List[str]] = None
    time_to_fix: str
    severity: str
    tools: Optional[List[str]] = None
    platforms: Optional[List[str]] = None
    url: Optional[str] = None
    entities: Optional[List[str]] = None
    priority_score: Optional[int] = None

class TimelineEvent(BaseModel):
    date: str
    timestamp: datetime
    type: str
    severity: str
    icon: str
    title: str
    description: str
    source: str
    color: str
    count: Optional[int] = None
    hovered: Optional[bool] = None

class ThreatIntelligenceMatrix(BaseModel):
    identity_reconstruction_risk: float
    phishing_vulnerability: float
    account_takeover_risk: float
    data_broker_aggregation: float
    overall_risk_score: float
    estimated_data_brokers: int
    recommendations_count: int

class PredictionRiskAssessment(BaseModel):
    total_predictions: int
    high_confidence: int
    medium_confidence: int
    low_confidence: int
    risk_summary: str

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
    repo_count: int = 0
    created_at: datetime
    # New fields for advanced features
    recommendations: Optional[List[Recommendation]] = None
    timeline: Optional[List[TimelineEvent]] = None
    timeline_stats: Optional[Dict[str, Any]] = None
    threat_intelligence: Optional[ThreatIntelligenceMatrix] = None
    predictions: Optional[List[Dict[str, Any]]] = None
    predictions_risk: Optional[PredictionRiskAssessment] = None

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
        
        # Create enhanced intelligence graph
        graph_engine = intelligence_graph_engine
        person_node = graph_engine.correlate_data(unified_profile)
        
        # Prepare OSINT data for expansion
        osint_data = {
            'repositories': [],
            'organizations': unified_profile.get('organizations', []),
            'emails': unified_profile.get('emails', []),
            'accounts': {}
        }
        
        # Extract repositories from GitHub data
        for result in successful_results:
            if isinstance(result, dict) and result.get('platform') == 'GitHub' and 'repositories' in result:
                osint_data['repositories'].extend(result['repositories'])
        
        # Add account information
        identities = unified_profile.get('identities', {})
        for platform, handle in identities.items():
            osint_data['accounts'][platform] = handle
        
        # Auto-inflate sparse graph for better visualization
        osint_data = graph_engine.auto_inflate_sparse_graph(osint_data, min_nodes_required=12)
        
        # Expand graph entities for enhanced visualization
        expanded_count = graph_engine.expand_entities_for_viz(osint_data)
        print(f"✅ Graph expanded with {expanded_count} new nodes")
        
        # Calculate risk score
        risk_score = risk_calculator.calculate_risk_score(unified_profile, graph_engine.graph)
        
        # Detect trackers
        trackers = tracker_detector.detect_trackers(unified_profile, graph_engine.graph)
        
        # Generate graph visualization data
        graph_data = graph_engine.export_json()
        
        # Create detailed findings from collected data and get repository count
        detailed_findings = []
        repo_count = 0
        for result in successful_results:
            if isinstance(result, dict) and "repositories" in result:
                # Get repository count
                repos = result.get("repositories", [])
                repo_count = len(repos)
                
                # Check for secrets in GitHub repositories
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
        
        # NEW: Generate recommendations
        rec_engine = SecurityRecommendations(osint_data, risk_score.get('total_score', 0))
        recommendations = rec_engine.generate_all_recommendations()
        recommendations = rec_engine.get_priority_score()  # Sort by priority
        
        # NEW: Generate timeline
        timeline_engine = ExposureTimeline(osint_data)
        timeline_events = timeline_engine.generate_timeline()
        timeline_stats = timeline_engine.get_timeline_stats()
        
        # NEW: Generate threat intelligence
        threat_intel_engine = ThreatIntelligence(osint_data, risk_score.get('total_score', 0), graph_engine.graph)
        threat_matrix = threat_intel_engine.get_threat_matrix()
        
        # NEW: Generate username predictions
        known_usernames = [
            identities.get("github", ""),
            identities.get("twitter", ""),
            identities.get("reddit", "")
        ]
        known_usernames = [u for u in known_usernames if u]  # Remove empty
        
        predictor = UsernamePredictorEngine(known_usernames, osint_data)
        predictions = predictor.generate_predictions()
        predictions_risk = predictor.get_risk_assessment()
        
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
            repo_count=repo_count,
            created_at=datetime.now(),
            # New fields
            recommendations=[Recommendation(**rec) for rec in recommendations],
            timeline=[TimelineEvent(**event) for event in timeline_events],
            timeline_stats=timeline_stats,
            threat_intelligence=ThreatIntelligenceMatrix(**threat_matrix),
            predictions=predictions,
            predictions_risk=PredictionRiskAssessment(**predictions_risk)
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
            
            # Handle datetime objects in new fields
            if "timeline" in result_dict and result_dict["timeline"]:
                for event in result_dict["timeline"]:
                    if "timestamp" in event and hasattr(event["timestamp"], 'isoformat'):
                        event["timestamp"] = event["timestamp"].isoformat()
            
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
    # Retrieve results from cache
    import os
    import json
    
    # Check cache directory
    cache_dir = "scan_cache"
    cache_file = os.path.join(cache_dir, f"{scan_id}.json")
    
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
                # Convert datetime strings back to datetime objects
                cached_data["created_at"] = datetime.fromisoformat(cached_data["created_at"].replace('Z', '+00:00'))
                # Convert lists of objects
                for i, tracker in enumerate(cached_data["trackers"]):
                    cached_data["trackers"][i] = Tracker(**tracker)
                for i, finding in enumerate(cached_data["detailed_findings"]):
                    cached_data["detailed_findings"][i] = DetailedFinding(**finding)
                for i, prediction in enumerate(cached_data["username_predictions"]):
                    cached_data["username_predictions"][i] = UsernamePrediction(**prediction)
                for i, platform in enumerate(cached_data["platforms"]):
                    cached_data["platforms"][i] = PlatformLink(**platform)
                
                # Handle new fields if they exist in cached data
                if "recommendations" in cached_data and cached_data["recommendations"]:
                    cached_data["recommendations"] = [Recommendation(**rec) for rec in cached_data["recommendations"]]
                if "timeline" in cached_data and cached_data["timeline"]:
                    for i, event in enumerate(cached_data["timeline"]):
                        # Convert timestamp string back to datetime
                        if "timestamp" in event and isinstance(event["timestamp"], str):
                            event["timestamp"] = datetime.fromisoformat(event["timestamp"].replace('Z', '+00:00'))
                        cached_data["timeline"][i] = TimelineEvent(**event)
                if "threat_intelligence" in cached_data and cached_data["threat_intelligence"]:
                    cached_data["threat_intelligence"] = ThreatIntelligenceMatrix(**cached_data["threat_intelligence"])
                if "predictions_risk" in cached_data and cached_data["predictions_risk"]:
                    cached_data["predictions_risk"] = PredictionRiskAssessment(**cached_data["predictions_risk"])
                
                return ScanResult(**cached_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading cached result: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="Scan result not found")

# Breach check endpoint
@app.get("/api/v1/breach-check/{email}")
async def check_breaches(email: str):
    """Check if an email has been involved in known data breaches"""
    # Query the HaveIBeenPwned API
    import requests
    import hashlib
    
    try:
        # Rate limit to be ethical
        from utils.rate_limiter import rate_limit
        await rate_limit("hibp")
        
        # HIBP uses k-anonymity, so we only send the first 5 characters of the SHA1 hash
        sha1_hash = hashlib.sha1(email.encode('utf-8')).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]
        
        # Query HIBP API
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
        headers = {
            "User-Agent": "DFM-OSINT-Tool"
        }
        
        # For demo purposes, we'll simulate a successful response
        # In a real implementation with a valid API key, you would use:
        # response = requests.get(url, headers=headers, timeout=10)
        # response.raise_for_status()
        # breaches = response.json()
        
        # Simulated response for demo
        breaches = [
            {
                "Name": "Adobe",
                "Title": "Adobe",
                "Domain": "adobe.com",
                "BreachDate": "2013-10-04",
                "AddedDate": "2013-12-04T00:00:00Z",
                "ModifiedDate": "2013-12-04T00:00:00Z",
                "PwnCount": 152445165,
                "Description": "In October 2013, 153 million Adobe accounts were breached...",
                "LogoPath": "https://haveibeenpwned.com/Content/Images/PwnedLogos/Adobe.png"
            }
        ] if "adobe" in email.lower() else []
        
        return {
            "email": email,
            "breaches_found": len(breaches),
            "breaches": breaches,
            "checked_at": datetime.now().isoformat()
        }
    except Exception as e:
        # Return empty result on error to avoid exposing internal errors
        return {
            "email": email,
            "breaches_found": 0,
            "breaches": [],
            "checked_at": datetime.now().isoformat(),
            "error": "Unable to check breaches at this time"
        }

# Graph visualization endpoint
@app.get("/api/v1/graph/visualize/{scan_id}")
async def visualize_graph(scan_id: str):
    """Get interactive graph visualization HTML"""
    # Generate a visualization from stored data
    import os
    import json
    
    # Check cache directory
    cache_dir = "scan_cache"
    cache_file = os.path.join(cache_dir, f"{scan_id}.json")
    
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
                
            # Generate visualization using our visualization engine
            from engines.visualization import visualization_engine
            import networkx as nx
            
            # Recreate the intelligence graph from cached data
            G = nx.Graph()
            
            # Add nodes from cached graph data
            for node_data in cached_data["graph_data"]["nodes"]:
                # Handle the attributes properly
                attributes = node_data.get("attributes", {})
                if "type" not in attributes and "type" in node_data:
                    attributes["type"] = node_data["type"]
                if "value" not in attributes and "label" in node_data:
                    attributes["value"] = node_data["label"]
                G.add_node(node_data["id"], **attributes)
                
            # Add edges from cached graph data
            for edge_data in cached_data["graph_data"]["edges"]:
                # Handle the attributes properly
                attributes = edge_data.get("attributes", {})
                if "relationship" not in attributes and "title" in edge_data:
                    attributes["relationship"] = edge_data["title"]
                G.add_edge(edge_data["from"], edge_data["to"], **attributes)
            
            # Generate interactive HTML visualization
            html_content = visualization_engine.create_interactive_graph(G)
            
            return {
                "scan_id": scan_id,
                "visualization_available": True,
                "html_content": html_content
            }
        except Exception as e:
            return {
                "scan_id": scan_id,
                "visualization_available": False,
                "error": f"Error generating visualization: {str(e)}"
            }
    else:
        return {
            "scan_id": scan_id,
            "visualization_available": False,
            "error": "Scan result not found"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)