"""
Setup Verification Script

This script verifies that all components of the OSINT system are properly installed and configured.
"""

import sys
import os
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Version 3.8+ required")
        return False

def check_import(module_name, package_name=None):
    """Check if a module can be imported"""
    try:
        if package_name:
            spec = importlib.util.find_spec(package_name)
            if spec is None:
                print(f"❌ {module_name} - Not installed")
                return False
        __import__(module_name)
        print(f"✅ {module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - Import failed: {e}")
        return False

def check_directory_structure():
    """Check if required directories exist"""
    print("Checking directory structure...")
    required_dirs = [
        "collectors",
        "utils"
    ]
    
    all_good = True
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name} - OK")
        else:
            print(f"❌ {dir_name} - Missing")
            all_good = False
    
    return all_good

def check_required_files():
    """Check if required files exist"""
    print("Checking required files...")
    required_files = [
        "main.py",
        "models.py",
        "config.py",
        "requirements.txt"
    ]
    
    all_good = True
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name} - OK")
        else:
            print(f"❌ {file_name} - Missing")
            all_good = False
    
    return all_good

def check_collector_modules():
    """Check if collector modules can be imported"""
    print("Checking collector modules...")
    collectors = [
        "collectors.github_collector",
        "collectors.linkedin_collector"
    ]
    
    all_good = True
    for collector in collectors:
        if not check_import(collector):
            all_good = False
    
    return all_good

def check_utility_modules():
    """Check if utility modules can be imported"""
    print("Checking utility modules...")
    utilities = [
        "utils.rate_limiter",
        "utils.secret_detector",
        "utils.tracker_detector",
        "utils.risk_calculator"
    ]
    
    all_good = True
    for utility in utilities:
        if not check_import(utility):
            all_good = False
    
    return all_good

def check_external_dependencies():
    """Check if external dependencies are available"""
    print("Checking external dependencies...")
    dependencies = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("pydantic", "pydantic"),
        ("networkx", "networkx"),
        ("pyvis", "pyvis"),
        ("sqlalchemy", "sqlalchemy"),
        ("requests", "requests"),
        ("email_validator", None)  # email-validator package imports as email_validator
    ]
    
    all_good = True
    for module_name, package_name in dependencies:
        if not check_import(module_name, package_name):
            all_good = False
    
    return all_good

def main():
    """Main verification function"""
    print("🔍 DFM OSINT System Setup Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Directory Structure", check_directory_structure),
        ("Required Files", check_required_files),
        ("External Dependencies", check_external_dependencies),
        ("Collector Modules", check_collector_modules),
        ("Utility Modules", check_utility_modules)
    ]
    
    results = []
    for check_name, check_function in checks:
        print(f"\n{check_name}:")
        print("-" * 30)
        result = check_function()
        results.append((check_name, result))
    
    print("\n" + "=" * 50)
    print("📋 Verification Summary:")
    print("=" * 50)
    
    all_passed = True
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! The system is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Start the backend: python main.py")
        print("   3. Run the frontend: npm run dev")
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
        print("\n🔧 Troubleshooting tips:")
        print("   • Install missing dependencies with pip")
        print("   • Check Python version (3.8+ required)")
        print("   • Verify all files are in place")
    
    print("=" * 50)

if __name__ == "__main__":
    main()