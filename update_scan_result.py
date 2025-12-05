with open('backend/main.py', 'r') as f:
    content = f.read()

# Replace the get_scan_result function implementation
old_impl = '''    # In production, this would retrieve results from a database
    raise HTTPException(status_code=404, detail="Scan result not found")'''

new_impl = '''    # Retrieve results from cache
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
                return ScanResult(**cached_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading cached result: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="Scan result not found")'''

content = content.replace(old_impl, new_impl)

with open('backend/main.py', 'w') as f:
    f.write(content)

print("Updated the get_scan_result function implementation")