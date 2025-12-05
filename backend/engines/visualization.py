"""Visualization Engine

This module generates interactive intelligence graphs using PyVis.
"""

from pyvis.network import Network
import networkx as nx
from typing import Dict, Any
import json
import random

class VisualizationEngine:
    def __init__(self):
        """Initialize the visualization engine"""
        pass
        
    def create_interactive_graph(self, intelligence_graph: nx.Graph) -> str:
        """
        Create an interactive HTML graph visualization
        
        Args:
            intelligence_graph (nx.Graph): Intelligence graph
            
        Returns:
            str: HTML string of the interactive graph
        """
        # Create PyVis network
        net = Network(
            height="600px", 
            width="100%", 
            bgcolor="#ffffff", 
            font_color="#000000"
        )
        
        # Set options for better visualization
        net.set_options("""
        {
          "nodes": {
            "shape": "dot",
            "size": 25,
            "font": {
              "size": 14
            }
          },
          "edges": {
            "color": {
              "inherit": true
            },
            "smooth": true
          },
          "physics": {
            "enabled": true,
            "stabilization": {
              "iterations": 100
            }
          }
        }
        """)
        
        # Add nodes with appropriate colors and sizes
        for node, data in intelligence_graph.nodes(data=True):
            node_type = data.get("type", "unknown")
            color = self._get_node_color(node_type)
            size = self._get_node_size(node_type)
            label = self._get_node_label(node, data)
            
            net.add_node(
                node, 
                label=label,
                color=color,
                size=size,
                title=self._get_node_tooltip(data)
            )
            
        # Add edges
        for source, target, data in intelligence_graph.edges(data=True):
            relationship = data.get("relationship", "connected")
            confidence = data.get("confidence", 0.5)
            width = max(1, int(confidence * 10))  # Width based on confidence
            color = self._get_edge_color(confidence)
            
            net.add_edge(
                source, 
                target, 
                title=relationship,
                width=width,
                color=color
            )
            
        # Generate HTML
        html = net.generate_html()
        return html
        
    def _get_node_color(self, node_type: str) -> str:
        """
        Get appropriate color for node type
        
        Args:
            node_type (str): Type of node
            
        Returns:
            str: Color code
        """
        color_map = {
            "user": "#FF6B6B",          # Red
            "identity": "#4ECDC4",      # Teal
            "location": "#45B7D1",      # Blue
            "organization": "#96CEB4",  # Green
            "website": "#FFEAA7",       # Yellow
            "email": "#DDA0DD",         # Plum
            "domain": "#98D8C8",        # Mint
            "unknown": "#CCCCCC"        # Gray
        }
        return color_map.get(node_type, "#999999")
        
    def _get_node_size(self, node_type: str) -> int:
        """
        Get appropriate size for node type
        
        Args:
            node_type (str): Type of node
            
        Returns:
            int: Node size
        """
        size_map = {
            "user": 35,
            "identity": 30,
            "location": 25,
            "organization": 25,
            "website": 20,
            "email": 20,
            "domain": 20,
            "unknown": 15
        }
        return size_map.get(node_type, 20)
        
    def _get_node_label(self, node_id: str, data: Dict[str, Any]) -> str:
        """
        Get appropriate label for node
        
        Args:
            node_id (str): Node ID
            data (Dict): Node data
            
        Returns:
            str: Node label
        """
        node_type = data.get("type", "unknown")
        
        if node_type == "user":
            return "Target User"
        elif node_type == "identity":
            return f"{data.get('platform', '')}:{data.get('handle', '')}"
        elif node_type == "location":
            return data.get("name", "Location")
        elif node_type == "organization":
            return data.get("name", "Organization")
        elif node_type == "website":
            return data.get("url", "Website")
        elif node_type == "email":
            return data.get("address", "Email")
        elif node_type == "domain":
            return data.get("name", "Domain")
        else:
            return node_id
            
    def _get_node_tooltip(self, data: Dict[str, Any]) -> str:
        """
        Get tooltip for node
        
        Args:
            data (Dict): Node data
            
        Returns:
            str: Tooltip text
        """
        tooltip_parts = []
        for key, value in data.items():
            if key not in ["type"] and value:
                tooltip_parts.append(f"{key}: {value}")
        return "\\n".join(tooltip_parts) if tooltip_parts else "No details"
        
    def _get_edge_color(self, confidence: float) -> str:
        """
        Get appropriate color for edge based on confidence
        
        Args:
            confidence (float): Confidence level (0.0-1.0)
            
        Returns:
            str: Color code
        """
        # Gradient from red (low confidence) to green (high confidence)
        if confidence >= 0.8:
            return "#00FF00"  # Green
        elif confidence >= 0.6:
            return "#90EE90"  # Light green
        elif confidence >= 0.4:
            return "#FFFF00"  # Yellow
        elif confidence >= 0.2:
            return "#FFA500"  # Orange
        else:
            return "#FF0000"  # Red
            
    def export_graph_data(self, intelligence_graph: nx.Graph) -> Dict[str, Any]:
        """
        Export graph data in JSON format for frontend consumption
        
        Args:
            intelligence_graph (nx.Graph): Intelligence graph
            
        Returns:
            Dict: Graph data in JSON format
        """
        nodes = []
        for node, data in intelligence_graph.nodes(data=True):
            nodes.append({
                "id": node,
                "label": self._get_node_label(node, data),
                "type": data.get("type", "unknown"),
                "color": self._get_node_color(data.get("type", "unknown")),
                "size": self._get_node_size(data.get("type", "unknown")),
                "attributes": {k: v for k, v in data.items() if k not in ["type"]}
            })
            
        edges = []
        for source, target, data in intelligence_graph.edges(data=True):
            edges.append({
                "from": source,
                "to": target,
                "title": data.get("relationship", "connected"),
                "width": max(1, int(data.get("confidence", 0.5) * 10)),
                "color": self._get_edge_color(data.get("confidence", 0.5)),
                "attributes": {k: v for k, v in data.items() if k not in ["relationship", "confidence"]}
            })
            
        return {
            "nodes": nodes,
            "edges": edges
        }

# Create a singleton instance
visualization_engine = VisualizationEngine()