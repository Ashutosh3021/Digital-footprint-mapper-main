with open('backend/main.py', 'r') as f:
    content = f.read()

# Replace the visualization function implementation
old_impl = '''# Graph visualization endpoint
@app.get("/api/v1/graph/visualize/{scan_id}")
async def visualize_graph(scan_id: str):
    """Get interactive graph visualization HTML"""
    # This would generate a visualization from stored data in production
    return {
        "scan_id": scan_id,
        "visualization_available": False,
        "message": "Graph visualization endpoint"
    }'''

new_impl = '''# Graph visualization endpoint
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
                G.add_node(node_data["id"], **node_data["attributes"])
                
            # Add edges from cached graph data
            for edge_data in cached_data["graph_data"]["edges"]:
                G.add_edge(edge_data["from"], edge_data["to"], **edge_data["attributes"])
            
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
        }'''

content = content.replace(old_impl, new_impl)

with open('backend/main.py', 'w') as f:
    f.write(content)

print("Updated the graph visualization function implementation")