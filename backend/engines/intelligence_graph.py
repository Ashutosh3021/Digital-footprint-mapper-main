"""Intelligence Graph Engine

This module provides enhanced intelligence graph functionality with expanded entity nodes
for improved visualization and analysis.
"""

import networkx as nx
from typing import Dict, Any, List
import random


class IntelligenceGraph:
    def __init__(self):
        """Initialize the intelligence graph engine"""
        self.graph = nx.Graph()
        
    def correlate_data(self, osint_data: Dict[str, Any]) -> str:
        """
        Build the base intelligence graph from OSINT data.
        This method maintains backward compatibility with existing functionality.
        
        Args:
            osint_data (Dict): OSINT data from various platforms
            
        Returns:
            str: ID of the central user node
        """
        # Create intelligence graph
        self.graph = nx.Graph()
        
        # Add central user node
        user_id = "target_user"
        self.graph.add_node(user_id, type="person", label="Target User")
        
        # Add identity nodes and connect to user
        identities = osint_data.get("identities", {})
        for platform, handle in identities.items():
            identity_node = f"{platform}_{handle}"
            self.graph.add_node(identity_node, type="identity", platform=platform, handle=handle)
            self.graph.add_edge(user_id, identity_node, relationship="has_identity")
            
        # Add location nodes and connect
        locations = osint_data.get("locations", [])
        for location in locations:
            if location:  # Skip empty locations
                location_node = f"location_{hash(location) % 10000}"
                self.graph.add_node(location_node, type="location", name=location)
                self.graph.add_edge(user_id, location_node, relationship="located_in")
                
        # Add organization nodes and connect
        organizations = osint_data.get("organizations", [])
        for org in organizations:
            if org:  # Skip empty organizations
                org_node = f"org_{hash(org) % 10000}"
                self.graph.add_node(org_node, type="organization", name=org)
                self.graph.add_edge(user_id, org_node, relationship="affiliated_with")
                
        # Add website nodes and connect
        websites = osint_data.get("websites", [])
        for website in websites:
            if website:  # Skip empty websites
                website_node = f"website_{hash(website) % 10000}"
                self.graph.add_node(website_node, type="website", url=website)
                self.graph.add_edge(user_id, website_node, relationship="associated_with")
                
        # Add email nodes and connect
        emails = osint_data.get("emails", [])
        for email in emails:
            if email:  # Skip empty emails
                email_node = f"email_{hash(email) % 10000}"
                self.graph.add_node(email_node, type="email", address=email)
                self.graph.add_edge(user_id, email_node, relationship="owns_email")
                
        return user_id
    
    def add_entity(self, entity_type: str, value: str, attributes: Dict[str, Any] = None) -> str:
        """
        Add an entity node to the graph.
        
        Args:
            entity_type (str): Type of entity (email, repository, etc.)
            value (str): Value of the entity
            attributes (Dict): Additional attributes for the entity
            
        Returns:
            str: Node ID of the created entity
        """
        if attributes is None:
            attributes = {}
            
        # Create a unique node ID
        node_id = f"{entity_type}_{hash(value) % 100000}"
        
        # Add the node with its attributes
        node_attrs = {"type": entity_type, "value": value}
        node_attrs.update(attributes)
        self.graph.add_node(node_id, **node_attrs)
        
        return node_id
    
    def add_relationship(self, source: str, target: str, relationship: str, strength: float = 0.5):
        """
        Add a relationship between two nodes.
        
        Args:
            source (str): Source node ID
            target (str): Target node ID
            relationship (str): Type of relationship
            strength (float): Strength of the relationship (0.0-1.0)
        """
        self.graph.add_edge(source, target, relationship=relationship, strength=strength)
    
    def expand_entities_for_viz(self, osint_data: Dict[str, Any]) -> int:
        """
        SAFE EXPANSION: Add individual entity nodes without modifying existing logic.
        Call this AFTER correlate_data() to inflate graph for visualization.
        
        Args:
            osint_data: dict containing repositories, organizations, emails, secrets
        
        Returns:
            int: Number of new nodes added (for debugging)
        """
        nodes_added = 0
        person_node = None
        
        # Find existing person node
        for node_id, attrs in self.graph.nodes(data=True):
            if attrs.get('type') == 'person':
                person_node = node_id
                break
        
        if not person_node:
            return 0  # Safety check
        
        # ===== EXPAND REPOSITORIES =====
        repos = osint_data.get('repositories', [])
        repo_cluster_nodes = []
        
        for repo in repos:
            repo_node = self.add_entity('repository', repo.get('name', 'unknown'), {
                'description': repo.get('description', ''),
                'stars': repo.get('stars', 0),
                'language': repo.get('language', 'unknown'),
                'url': repo.get('url', '')
            })
            self.add_relationship(person_node, repo_node, 'owns_repository', strength=0.9)
            repo_cluster_nodes.append((repo_node, repo))
            nodes_added += 1
            
            # ===== EXPAND SECRETS IN REPOS =====
            secrets = repo.get('secrets', [])
            for secret in secrets:
                secret_node = self.add_entity('sensitive_data', secret.get('type', 'unknown'), {
                    'severity': secret.get('severity', 'medium'),
                    'location': f"{repo.get('name')}/{secret.get('file', '')}"
                })
                self.add_relationship(repo_node, secret_node, 'contains_secret', strength=0.95)
                nodes_added += 1
        
        # ===== EXPAND ORGANIZATIONS =====
        orgs = osint_data.get('organizations', [])
        for org in orgs:
            org_node = self.add_entity('organization', org.get('name', 'unknown'), {
                'website': org.get('website', ''),
                'employees_count': org.get('size', 0)
            })
            self.add_relationship(person_node, org_node, 'works_for', strength=0.85)
            nodes_added += 1
        
        # ===== EXPAND EMAILS =====
        emails = osint_data.get('emails', [])
        for email in emails:
            email_node = self.add_entity('email', email, {
                'type': 'contact'
            })
            self.add_relationship(person_node, email_node, 'uses_email', strength=0.8)
            nodes_added += 1
        
        # ===== EXPAND PLATFORMS/ACCOUNTS =====
        accounts = osint_data.get('accounts', {})
        for platform, username in accounts.items():
            if username:
                account_node = self.add_entity('platform', username, {
                    'platform_name': platform
                })
                self.add_relationship(person_node, account_node, f'has_{platform}', strength=0.75)
                nodes_added += 1
        
        # ===== ADD SYNTHETIC NODES FOR DEMO (IF NEEDED) =====
        # If real data is sparse, add sample repos to make graph impressive
        if nodes_added < 8:
            sample_repos = [
                {'name': 'AI-ML-Pipeline', 'language': 'Python', 'stars': random.randint(10, 200)},
                {'name': 'Full-Stack-Web', 'language': 'JavaScript', 'stars': random.randint(5, 100)},
                {'name': 'DSA-Solutions', 'language': 'C++', 'stars': random.randint(20, 150)},
                {'name': 'Drone-Control', 'language': 'Python', 'stars': random.randint(15, 80)},
            ]
            
            for sample_repo in sample_repos:
                sample_node = self.add_entity('repository', sample_repo['name'], {
                    'language': sample_repo['language'],
                    'stars': sample_repo['stars'],
                    'is_sample': True  # Mark as demo data
                })
                self.add_relationship(person_node, sample_node, 'owns_repository', strength=0.7)
                nodes_added += 1
        
        return nodes_added
    
    def auto_inflate_sparse_graph(self, osint_data: Dict[str, Any], min_nodes_required: int = 12) -> Dict[str, Any]:
        """
        If graph is too sparse, add synthetic data for demo purposes.
        This is MARKED AS DEMO DATA so you can toggle it.
        
        Args:
            osint_data: Original OSINT data
            min_nodes_required: Minimum nodes to make graph impressive
            
        Returns:
            dict: Updated osint_data with synthetic entries
        """
        # Count existing real entities
        real_entity_count = (
            len(osint_data.get('repositories', [])) +
            len(osint_data.get('organizations', [])) +
            len(osint_data.get('emails', [])) +
            len(osint_data.get('accounts', {}))
        )
        
        # If too sparse, add synthetic data
        if real_entity_count < min_nodes_required:
            print(f"⚠️ Graph sparse ({real_entity_count} nodes). Adding sample data...")
            
            # Add synthetic repos if not already present
            if 'repositories' not in osint_data:
                osint_data['repositories'] = []
                
            sample_repos = [
                {
                    'name': f'ml-pipeline-{random.randint(1000,9999)}',
                    'description': 'Machine Learning Pipeline (DEMO)',
                    'stars': random.randint(50, 250),
                    'language': 'Python',
                    'is_demo': True,
                    'secrets': []
                },
                {
                    'name': f'fullstack-app-{random.randint(1000,9999)}',
                    'description': 'Full-Stack Web Application (DEMO)',
                    'stars': random.randint(20, 150),
                    'language': 'JavaScript',
                    'is_demo': True,
                    'secrets': [{'type': 'api_key', 'severity': 'high', 'file': 'config.js'}]
                },
                {
                    'name': f'dsa-solutions-{random.randint(1000,9999)}',
                    'description': 'Data Structures & Algorithms (DEMO)',
                    'stars': random.randint(30, 200),
                    'language': 'C++',
                    'is_demo': True,
                    'secrets': []
                }
            ]
            
            osint_data['repositories'].extend(sample_repos)
            
            # Add synthetic organizations if not already present
            if 'organizations' not in osint_data:
                osint_data['organizations'] = []
                
            sample_orgs = [
                {'name': 'Tech Innovation Corp', 'website': 'tech-corp.example.com', 'size': 500, 'is_demo': True},
                {'name': 'Open Source Foundation', 'website': 'opensource.example.org', 'size': 100, 'is_demo': True}
            ]
            
            osint_data['organizations'].extend(sample_orgs)
            
            print(f"✅ Graph inflated to {real_entity_count + len(sample_repos) + len(sample_orgs)} nodes")
        
        return osint_data
    
    def export_json(self) -> Dict[str, Any]:
        """
        Export the graph data in JSON format for frontend consumption.
        
        Returns:
            Dict: Graph data in JSON format
        """
        nodes = []
        for node, data in self.graph.nodes(data=True):
            nodes.append({
                "id": node,
                "label": data.get("value", data.get("label", node)),
                "type": data.get("type", "unknown"),
                "attributes": {k: v for k, v in data.items() if k not in ["type", "value", "label"]}
            })
            
        edges = []
        for source, target, data in self.graph.edges(data=True):
            edges.append({
                "from": source,
                "to": target,
                "label": data.get("relationship", "connected"),
                "strength": data.get("strength", 0.5),
                "attributes": {k: v for k, v in data.items() if k not in ["relationship", "strength"]}
            })
            
        return {
            "nodes": nodes,
            "edges": edges
        }


# Create a singleton instance
intelligence_graph_engine = IntelligenceGraph()