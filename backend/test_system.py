"""
System Test Script

This script performs a basic test of the OSINT system functionality.
"""

import asyncio
import sys
import os

# Add the collectors directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'collectors'))

from collectors.github_collector import GitHubCollector
from collectors.linkedin_collector import LinkedInCollector

async def test_collectors():
    """Test the data collectors"""
    print("Testing GitHub Collector...")
    try:
        github_collector = GitHubCollector()
        # Test with GitHub's test user
        result = await github_collector.collect_all_data("octocat")
        print("✅ GitHub Collector: SUCCESS")
        print(f"   Collected data for: {result.get('profile', {}).get('name', 'Unknown')}")
    except Exception as e:
        print(f"❌ GitHub Collector: FAILED - {e}")
    
    print("\nTesting LinkedIn Collector...")
    try:
        linkedin_collector = LinkedInCollector()
        # Test with a sample URL
        result = await linkedin_collector.collect_all_data("https://linkedin.com/in/testuser")
        print("✅ LinkedIn Collector: SUCCESS")
        print(f"   Collected data for: {result.get('profile', {}).get('name', 'Unknown')}")
    except Exception as e:
        print(f"❌ LinkedIn Collector: FAILED - {e}")

def test_imports():
    """Test that all modules can be imported"""
    print("Testing Module Imports...")
    
    modules_to_test = [
        ("collectors.github_collector", "GitHub Collector"),
        ("collectors.linkedin_collector", "LinkedIn Collector"),
        ("utils.rate_limiter", "Rate Limiter"),
        ("utils.secret_detector", "Secret Detector"),
        ("utils.tracker_detector", "Tracker Detector"),
        ("utils.risk_calculator", "Risk Calculator")
    ]
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {description}: IMPORT SUCCESS")
        except Exception as e:
            print(f"❌ {description}: IMPORT FAILED - {e}")

def main():
    """Main test function"""
    print("🔍 DFM OSINT System Test")
    print("=" * 40)
    
    # Test imports
    test_imports()
    
    print("\n" + "-" * 40)
    
    # Test collectors
    asyncio.run(test_collectors())
    
    print("\n" + "=" * 40)
    print("🏁 System Test Complete!")
    print("\nNext steps:")
    print("1. Start the backend: python main.py")
    print("2. Start the frontend: npm run dev")
    print("3. Visit http://localhost:3000 in your browser")

if __name__ == "__main__":
    main()