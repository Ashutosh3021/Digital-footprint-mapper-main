"""Test script for the enhanced IntelligenceGraph implementation."""

from engines.intelligence_graph import IntelligenceGraph
import json

def test_intelligence_graph():
    """Test the enhanced IntelligenceGraph functionality."""
    # Create an instance of the IntelligenceGraph
    graph_engine = IntelligenceGraph()
    
    # Sample OSINT data
    osint_data = {
        "identities": {
            "github": "testuser",
            "linkedin": "test-user",
            "twitter": "testuser123"
        },
        "personal_info": {
            "name": "Test User",
            "bio": "Software developer and cybersecurity enthusiast"
        },
        "organizations": ["TestCorp", "OpenSourceOrg"],
        "emails": ["test@example.com", "test.user@company.com"],
        "websites": ["https://testuser.dev", "https://blog.testuser.dev"],
        "locations": ["San Francisco, CA", "New York, NY"]
    }
    
    # Test the correlate_data method
    person_node = graph_engine.correlate_data(osint_data)
    print(f"Created base graph with person node: {person_node}")
    print(f"Base graph has {len(graph_engine.graph.nodes)} nodes and {len(graph_engine.graph.edges)} edges")
    
    # Add enhanced OSINT data for expansion
    enhanced_osint_data = {
        'repositories': [
            {
                'name': 'awesome-project',
                'description': 'An awesome project',
                'stars': 42,
                'language': 'Python',
                'url': 'https://github.com/testuser/awesome-project',
                'secrets': [
                    {
                        'type': 'api_key',
                        'severity': 'high',
                        'file': 'config.py'
                    }
                ]
            },
            {
                'name': 'test-repo',
                'description': 'A test repository',
                'stars': 10,
                'language': 'JavaScript',
                'url': 'https://github.com/testuser/test-repo',
                'secrets': []
            }
        ],
        'organizations': [
            {'name': org, 'website': f'https://www.{org.lower()}.com', 'size': 100} 
            for org in osint_data["organizations"]
        ],
        'emails': osint_data["emails"],
        'accounts': osint_data["identities"]
    }
    
    # Test auto inflation
    enhanced_osint_data = graph_engine.auto_inflate_sparse_graph(enhanced_osint_data, min_nodes_required=5)
    print(f"After auto inflation, repositories: {len(enhanced_osint_data['repositories'])}")
    
    # Test entity expansion
    expanded_count = graph_engine.expand_entities_for_viz(enhanced_osint_data)
    print(f"Expanded graph with {expanded_count} new nodes")
    print(f"Enhanced graph has {len(graph_engine.graph.nodes)} nodes and {len(graph_engine.graph.edges)} edges")
    
    # Test export functionality
    graph_data = graph_engine.export_json()
    print(f"Exported graph with {len(graph_data['nodes'])} nodes and {len(graph_data['edges'])} edges")
    
    # Print some node information
    print("\nSample nodes:")
    for i, node in enumerate(graph_data['nodes'][:5]):
        print(f"  {i+1}. {node['type']}: {node['label']}")
    
    print("\nSample edges:")
    for i, edge in enumerate(graph_data['edges'][:5]):
        print(f"  {i+1}. {edge['from']} -> {edge['to']} ({edge['label']})")
    
    # Verify we have the expected node types
    node_types = [node['type'] for node in graph_data['nodes']]
    expected_types = ['person', 'repository', 'sensitive_data', 'organization', 'email']
    
    print(f"\nNode types found: {set(node_types)}")
    
    for expected_type in expected_types:
        count = node_types.count(expected_type)
        print(f"  {expected_type}: {count} nodes")
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_intelligence_graph()