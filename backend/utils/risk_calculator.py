"""Risk Calculator Utility

This module provides functionality to calculate risk scores based on
OSINT findings, platform usage, and other factors.
"""

from typing import List, Dict, Any

class RiskCalculator:
    def __init__(self):
        """Initialize risk calculator with default weights"""
        self.weights = {
            "data_sensitivity": 0.4,
            "cross_platform": 0.25,
            "recency": 0.2,
            "exploitability": 0.15
        }
    
    def calculate_risk_score(self, findings: List[Dict[str, Any]], 
                           platforms: List[Dict[str, Any]], 
                           breaches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate comprehensive risk score
        
        Args:
            findings (List[Dict]): Security findings
            platforms (List[Dict]): Linked platforms
            breaches (List[Dict]): Data breaches
            
        Returns:
            Dict containing risk score and breakdown
        """
        # Calculate data sensitivity score
        data_sensitivity = self._calculate_data_sensitivity(findings)
        
        # Calculate cross-platform correlation score
        cross_platform = self._calculate_cross_platform(platforms)
        
        # Calculate recency score
        recency = self._calculate_recency(findings)
        
        # Calculate exploitability score
        exploitability = self._calculate_exploitability(findings, platforms)
        
        # Calculate weighted total score
        total_score = (
            data_sensitivity * self.weights["data_sensitivity"] +
            cross_platform * self.weights["cross_platform"] +
            recency * self.weights["recency"] +
            exploitability * self.weights["exploitability"]
        )
        
        # Determine severity level
        severity = self._determine_severity(total_score)
        
        return {
            "total_score": round(total_score, 2),
            "severity": severity,
            "breakdown": {
                "data_sensitivity": round(data_sensitivity, 2),
                "cross_platform": round(cross_platform, 2),
                "recency": round(recency, 2),
                "exploitability": round(exploitability, 2)
            }
        }
    
    def _calculate_data_sensitivity(self, findings: List[Dict[str, Any]]) -> float:
        """Calculate data sensitivity score"""
        score = 0
        for finding in findings:
            severity = finding.get("severity", "low")
            if severity == "critical":
                score += 40
            elif severity == "high":
                score += 25
            elif severity == "medium":
                score += 10
            elif severity == "low":
                score += 5
        return min(score, 100)
    
    def _calculate_cross_platform(self, platforms: List[Dict[str, Any]]) -> float:
        """Calculate cross-platform correlation score"""
        platform_count = len(platforms)
        # Each additional platform adds 5 points up to 25 max
        return min(platform_count * 5, 25)
    
    def _calculate_recency(self, findings: List[Dict[str, Any]]) -> float:
        """Calculate data recency score"""
        # In a real implementation, this would check timestamps
        # For now, we'll use a default score
        return 50
    
    def _calculate_exploitability(self, findings: List[Dict[str, Any]], 
                                platforms: List[Dict[str, Any]]) -> float:
        """Calculate exploitability score"""
        score = 0
        platform_count = len(platforms)
        
        # Combinations enable attacks
        if platform_count >= 3:
            score += 20
            
        # Check for critical findings
        for finding in findings:
            if finding.get("severity") == "critical":
                score += 30
            elif finding.get("severity") == "high":
                score += 15
                
        return min(score, 100)
    
    def _determine_severity(self, score: float) -> str:
        """Determine severity level"""
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

# Global risk calculator instance
risk_calculator = RiskCalculator()

def calculate_risk_score(findings: List[Dict[str, Any]], 
                        platforms: List[Dict[str, Any]], 
                        breaches: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate risk score"""
    return risk_calculator.calculate_risk_score(findings, platforms, breaches)