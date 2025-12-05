"""Entity Resolution Engine

This module handles the identification of shared attributes across platforms
and creation of correlation edges in the intelligence graph.
"""

import networkx as nx
from typing import Dict, List, Any, Set, Tuple
from datetime import datetime
import re

class EntityResolutionEngine:
    def __init__(self):
        """Initialize the entity resolution engine"""
        pass
        
    def resolve_entities(self, unified_profile: Dict[str, Any]) -> nx.Graph:
        """
        Resolve entities and create correlation graph
        
        Args:
            unified_profile (Dict): Unified user profile from data fusion
            
        Returns:
            nx.Graph: Intelligence graph with resolved entities and correlations
        """
        # Create intelligence graph
        G = nx.Graph()
        
        # Add central user node
        user_id = "target_user"
        G.add_node(user_id, type="user", label="Target User")
        
        # Add identity nodes and connect to user
        identities = unified_profile.get("identities", {})
        for platform, handle in identities.items():
            identity_node = f"{platform}_{handle}"
            G.add_node(identity_node, type="identity", platform=platform, handle=handle)
            G.add_edge(user_id, identity_node, relationship="has_identity")
            
        # Add location nodes and connect
        locations = unified_profile.get("locations", [])
        for location in locations:
            if location:  # Skip empty locations
                location_node = f"location_{hash(location) % 10000}"
                G.add_node(location_node, type="location", name=location)
                G.add_edge(user_id, location_node, relationship="located_in")
                
        # Add organization nodes and connect
        organizations = unified_profile.get("organizations", [])
        for org in organizations:
            if org:  # Skip empty organizations
                org_node = f"org_{hash(org) % 10000}"
                G.add_node(org_node, type="organization", name=org)
                G.add_edge(user_id, org_node, relationship="affiliated_with")
                
        # Add website nodes and connect
        websites = unified_profile.get("websites", [])
        for website in websites:
            if website:  # Skip empty websites
                website_node = f"website_{hash(website) % 10000}"
                G.add_node(website_node, type="website", url=website)
                G.add_edge(user_id, website_node, relationship="associated_with")
                
        # Add email nodes and connect
        emails = unified_profile.get("emails", [])
        for email in emails:
            if email:  # Skip empty emails
                email_node = f"email_{hash(email) % 10000}"
                G.add_node(email_node, type="email", address=email)
                G.add_edge(user_id, email_node, relationship="owns_email")
                
        # Add repository nodes from GitHub data
        self._add_repository_nodes(G, unified_profile)
        
        # Identify cross-platform correlations
        self._identify_correlations(G, unified_profile)
        
        return G
        
    def _identify_correlations(self, graph: nx.Graph, unified_profile: Dict[str, Any]):
        """
        Identify correlations between entities across platforms
        
        Args:
            graph (nx.Graph): Intelligence graph
            unified_profile (Dict): Unified user profile
        """
        # Get all identity nodes
        identity_nodes = [n for n, attr in graph.nodes(data=True) 
                         if attr.get("type") == "identity"]
                         
        # Correlate based on shared domains
        self._correlate_by_domain(graph, identity_nodes, unified_profile)
        
        # Correlate based on similar names/bios
        self._correlate_by_similarity(graph, identity_nodes, unified_profile)
        
        # Correlate based on location overlap
        self._correlate_by_location(graph, identity_nodes, unified_profile)
        
    def _correlate_by_domain(self, graph: nx.Graph, identity_nodes: List[str], 
                           unified_profile: Dict[str, Any]):
        """
        Correlate identities based on shared email domains
        
        Args:
            graph (nx.Graph): Intelligence graph
            identity_nodes (List[str]): Identity nodes
            unified_profile (Dict): Unified user profile
        """
        # Extract email domains
        emails = unified_profile.get("emails", [])
        domains = set()
        for email in emails:
            if "@" in email:
                domain = email.split("@")[1]
                domains.add(domain)
                
        # Connect identities that share domains
        for domain in domains:
            domain_identities = []
            for node in identity_nodes:
                # For simplicity, we'll assume any identity could potentially
                # be associated with any domain (in reality, this would be more specific)
                domain_identities.append(node)
                
            # Create domain node and connect identities
            if len(domain_identities) > 1:
                domain_node = f"domain_{domain}"
                graph.add_node(domain_node, type="domain", name=domain)
                
                for identity_node in domain_identities:
                    graph.add_edge(identity_node, domain_node, 
                                 relationship="associated_with_domain", 
                                 confidence=0.7)
                    
    def _correlate_by_similarity(self, graph: nx.Graph, identity_nodes: List[str], 
                               unified_profile: Dict[str, Any]):
        """
        Correlate identities based on similar names or bios
        
        Args:
            graph (nx.Graph): Intelligence graph
            identity_nodes (List[str]): Identity nodes
            unified_profile (Dict): Unified user profile
        """
        # Extract names and bios
        names = []
        bios = []
        
        personal_info = unified_profile.get("personal_info", {})
        if personal_info.get("name"):
            names.append(personal_info["name"])
        if personal_info.get("bio"):
            bios.append(personal_info["bio"])
            
        # Simple similarity check (in practice, you'd use more sophisticated NLP)
        if len(names) > 1:
            # Names are similar if they share significant substrings
            for i in range(len(names)):
                for j in range(i+1, len(names)):
                    if self._names_similar(names[i], names[j]):
                        # Add high confidence edge
                        pass  # Would connect nodes in a real implementation
                        
        if len(bios) > 1:
            # Bios are similar if they share keywords
            for i in range(len(bios)):
                for j in range(i+1, len(bios)):
                    if self._bios_similar(bios[i], bios[j]):
                        # Add medium confidence edge
                        pass  # Would connect nodes in a real implementation
                        
    def _add_repository_nodes(self, graph: nx.Graph, unified_profile: Dict[str, Any]):
        """
        Add repository nodes to the graph
        
        Args:
            graph (nx.Graph): Intelligence graph
            unified_profile (Dict): Unified user profile
        """
        # This method would add repository nodes if we had access to them
        # In the current implementation, repositories are processed separately
        # for secret detection but not added to the intelligence graph
        pass
        
    def _correlate_by_location(self, graph: nx.Graph, identity_nodes: List[str], 
                             unified_profile: Dict[str, Any]):
        """
        Correlate identities based on shared locations
        
        Args:
            graph (nx.Graph): Intelligence graph
            identity_nodes (List[str]): Identity nodes
            unified_profile (Dict): Unified user profile
        """
        # In a real implementation, this would connect identities that share locations
        # For now, we'll just note that this correlation is possible
        pass
        
    def _names_similar(self, name1: str, name2: str) -> bool:
        """
        Check if two names are similar
        
        Args:
            name1 (str): First name
            name2 (str): Second name
            
        Returns:
            bool: True if names are similar
        """
        # Simple implementation - in practice, use fuzzy matching or NLP
        name1_clean = re.sub(r'[^\w\s]', '', name1.lower())
        name2_clean = re.sub(r'[^\w\s]', '', name2.lower())
        
        # Check if one name contains the other or they share significant words
        words1 = set(name1_clean.split())
        words2 = set(name2_clean.split())
        
        common_words = words1.intersection(words2)
        return len(common_words) > 0
        
    def _bios_similar(self, bio1: str, bio2: str) -> bool:
        """
        Check if two bios are similar
        
        Args:
            bio1 (str): First bio
            bio2 (str): Second bio
            
        Returns:
            bool: True if bios are similar
        """
        # Simple implementation - in practice, use TF-IDF or other NLP techniques
        bio1_clean = re.sub(r'[^\w\s]', '', bio1.lower())
        bio2_clean = re.sub(r'[^\w\s]', '', bio2.lower())
        
        # Check for common words
        words1 = set(bio1_clean.split())
        words2 = set(bio2_clean.split())
        
        common_words = words1.intersection(words2)
        return len(common_words) >= 3  # At least 3 common words

# Create a singleton instance
entity_resolution_engine = EntityResolutionEngine()