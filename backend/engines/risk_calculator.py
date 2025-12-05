"""Risk Calculator Engine

This module calculates risk scores based on OSINT findings using weighted factors:
- Data sensitivity
- Cross-platform correlation
- Data recency
- Exploitability
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
import networkx as nx

class RiskCalculator:
    def __init__(self):
        """Initialize the risk calculator with default weights"""
        self.weights = {
            "data_sensitivity": 0.4,
            "cross_platform": 0.25,
            "recency": 0.2,
            "exploitability": 0.15
        }
        
    def calculate_risk_score(self, unified_profile: Dict[str, Any], 
                           intelligence_graph: nx.Graph) -> Dict[str, Any]:
        """
        Calculate comprehensive risk score
        
        Args:
            unified_profile (Dict): Unified user profile
            intelligence_graph (nx.Graph): Intelligence graph with correlations
            
        Returns:
            Dict containing risk score and breakdown
        """
        # Calculate individual factor scores
        data_sensitivity_score = self._calculate_data_sensitivity_score(unified_profile)
        cross_platform_score = self._calculate_cross_platform_score(intelligence_graph)
        recency_score = self._calculate_recency_score(unified_profile)
        exploitability_score = self._calculate_exploitability_score(unified_profile, intelligence_graph)
        
        # Calculate weighted total score
        total_score = (
            data_sensitivity_score * self.weights["data_sensitivity"] +
            cross_platform_score * self.weights["cross_platform"] +
            recency_score * self.weights["recency"] +
            exploitability_score * self.weights["exploitability"]
        )
        
        # Determine severity level
        severity = self._determine_severity(total_score)
        
        return {
            "total_score": round(total_score, 2),
            "severity": severity,
            "breakdown": {
                "data_sensitivity": round(data_sensitivity_score, 2),
                "cross_platform_correlation": round(cross_platform_score, 2),
                "data_recency": round(recency_score, 2),
                "exploitability": round(exploitability_score, 2)
            },
            "calculated_at": datetime.now().isoformat()
        }
        
    def _calculate_data_sensitivity_score(self, unified_profile: Dict[str, Any]) -> float:
        """
        Calculate data sensitivity score based on exposed sensitive information
        
        Args:
            unified_profile (Dict): Unified user profile
            
        Returns:
            float: Data sensitivity score (0-100)
        """
        score = 0
        
        # Check for exposed emails
        emails = unified_profile.get("emails", [])
        if emails:
            score += len(emails) * 15  # 15 points per email
            
        # Check for social media presence (indicates public exposure)
        identities = unified_profile.get("identities", {})
        score += len(identities) * 10  # 10 points per platform
        
        # Check for professional information (higher risk in targeted attacks)
        professional_info = unified_profile.get("professional_info", {})
        if professional_info.get("headline") or professional_info.get("role"):
            score += 20  # 20 points for professional info
            
        # Cap at 100
        return min(score, 100)
        
    def _calculate_cross_platform_score(self, intelligence_graph: nx.Graph) -> float:
        """
        Calculate cross-platform correlation score
        
        Args:
            intelligence_graph (nx.Graph): Intelligence graph
            
        Returns:
            float: Cross-platform correlation score (0-100)
        """
        # Count identities (platform presences)
        identity_nodes = [n for n, attr in intelligence_graph.nodes(data=True) 
                         if attr.get("type") == "identity"]
        
        # Score based on number of platforms (max 25 points)
        platform_count = len(identity_nodes)
        return min(platform_count * 5, 25)  # 5 points per platform, max 25
        
    def _calculate_recency_score(self, unified_profile: Dict[str, Any]) -> float:
        """
        Calculate data recency score based on how recently data was collected
        
        Args:
            unified_profile (Dict): Unified user profile
            
        Returns:
            float: Data recency score (0-100)
        """
        collected_at_str = unified_profile.get("collected_at")
        if not collected_at_str:
            return 50  # Default middle score
            
        try:
            collected_at = datetime.fromisoformat(collected_at_str.replace('Z', '+00:00'))
            days_old = (datetime.now(collected_at.tzinfo) - collected_at).days
            
            # More recent data = higher risk
            # 0-30 days: 100 points
            # 31-90 days: 75 points
            # 91-180 days: 50 points
            # 181-365 days: 25 points
            # >365 days: 10 points
            
            if days_old <= 30:
                return 100
            elif days_old <= 90:
                return 75
            elif days_old <= 180:
                return 50
            elif days_old <= 365:
                return 25
            else:
                return 10
                
        except Exception:
            return 50  # Default score if parsing fails
            
    def _calculate_exploitability_score(self, unified_profile: Dict[str, Any], 
                                     intelligence_graph: nx.Graph) -> float:
        """
        Calculate exploitability score based on combinations of data
        
        Args:
            unified_profile (Dict): Unified user profile
            intelligence_graph (nx.Graph): Intelligence graph
            
        Returns:
            float: Exploitability score (0-100)
        """
        score = 0
        
        # Check for email + professional info (enables phishing)
        emails = unified_profile.get("emails", [])
        professional_info = unified_profile.get("professional_info", {})
        if emails and (professional_info.get("headline") or professional_info.get("role")):
            score += 40  # High risk for phishing
            
        # Check for location data (enables physical targeting)
        locations = unified_profile.get("locations", [])
        if locations:
            score += 20  # Medium risk for physical targeting
            
        # Check for social media connections (enables social engineering)
        identities = unified_profile.get("identities", {})
        if len(identities) >= 3:
            score += 20  # Medium risk for social engineering
            
        # Check for correlated identities (higher exploitability)
        identity_nodes = [n for n, attr in intelligence_graph.nodes(data=True) 
                         if attr.get("type") == "identity"]
        if len(identity_nodes) >= 2:
            # Look for strong correlation edges
            strong_correlations = 0
            for node in identity_nodes:
                for neighbor in intelligence_graph.neighbors(node):
                    edge_data = intelligence_graph.get_edge_data(node, neighbor)
                    if edge_data and edge_data.get("confidence", 0) > 0.7:
                        strong_correlations += 1
                        
            score += min(strong_correlations * 10, 20)  # Up to 20 points for strong correlations
            
        return min(score, 100)
        
    def _determine_severity(self, score: float) -> str:
        """
        Determine severity level based on score
        
        Args:
            score (float): Risk score
            
        Returns:
            str: Severity level
        """
        if score >= 80:
            return "Critical"
        elif score >= 60:
            return "High"
        elif score >= 40:
            return "Medium"
        elif score >= 20:
            return "Low"
        else:
            return "Minimal"

# Create a singleton instance
risk_calculator = RiskCalculator()