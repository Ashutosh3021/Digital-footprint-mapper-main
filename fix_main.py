with open('backend/main.py', 'r') as f:
    content = f.read()

# Fix the formatting issue
content = content.replace(
    'detail=f"Scan failed: {str(e)}")# Get scan result endpoint',
    'detail=f"Scan failed: {str(e)}")\n\n# Get scan result endpoint'
)

with open('backend/main.py', 'w') as f:
    f.write(content)

print("Fixed the formatting issue in main.py")