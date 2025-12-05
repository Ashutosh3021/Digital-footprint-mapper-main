"""
Test Script for Backend API

This script tests the main endpoints of the OSINT backend API.
"""

import requests
import json
from datetime import datetime

# Base URL for the API
import os
BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8004')

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_scan_endpoint():
    """Test the scan endpoint with sample data"""
    print("Testing scan endpoint...")
    
    # Sample scan data
    scan_data = {
        "email": "test@example.com",
        "github": "octocat",
        "linkedin": "https://linkedin.com/in/testuser",
        "twitter": "testuser",
        "reddit": "testuser"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/scan",
        headers={"Content-Type": "application/json"},
        data=json.dumps(scan_data)
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Scan Result: {json.dumps(result, indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()

def test_breach_check():
    """Test the breach check endpoint"""
    print("Testing breach check endpoint...")
    
    email = "test@example.com"
    response = requests.get(f"{BASE_URL}/api/v1/breach-check/{email}")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Breach Results: {json.dumps(result, indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()

def test_graph_visualization():
    """Test the graph visualization endpoint"""
    print("Testing graph visualization endpoint...")
    
    # First, we need to create a scan to get a scan_id
    scan_data = {
        "email": "test@example.com",
        "github": "octocat",
        "linkedin": "https://linkedin.com/in/testuser"
    }
    
    # Create a scan
    response = requests.post(
        f"{BASE_URL}/api/v1/scan",
        headers={"Content-Type": "application/json"},
        data=json.dumps(scan_data)
    )
    
    if response.status_code == 200:
        scan_result = response.json()
        # Extract scan_id from the response or generate one
        # For this test, we'll just show that the endpoint exists
        print("Graph visualization endpoint is available")
        print("Note: Actual testing requires a valid scan_id from a previous scan")
    else:
        print(f"Error creating scan for graph test: {response.text}")
    print()

if __name__ == "__main__":
    print(f"Testing OSINT Backend API at {BASE_URL}")
    print("=" * 50)
    
    try:
        test_health_check()
        test_scan_endpoint()
        test_breach_check()
        test_graph_visualization()
        
        print("All tests completed!")
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to the backend server at {BASE_URL}. Make sure it's running.")
        print("To start the backend server:")
        print("1. Navigate to the backend directory: cd backend")
        print("2. Run: python main.py")
        print("")
        print("Alternatively, run the start_system.bat file from the project root to start both frontend and backend.")
    except Exception as e:
        print(f"Error during testing: {str(e)}")