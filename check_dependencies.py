#!/usr/bin/env python3
"""
Check if all required dependencies are installed
"""

import sys

def check_import(package_name, import_name=None):
    """Check if a package can be imported"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name}")
        return True
    except ImportError:
        print(f"❌ {package_name} - NOT INSTALLED")
        return False

def main():
    print("=" * 60)
    print("🔍 Checking Dependencies...")
    print("=" * 60)
    print()
    
    dependencies = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("openai", "openai"),
        ("python-dotenv", "dotenv"),
        ("python-multipart", "multipart"),
        ("requests", "requests"),
    ]
    
    all_installed = True
    
    for package_name, import_name in dependencies:
        if not check_import(package_name, import_name):
            all_installed = False
    
    print()
    print("=" * 60)
    
    if all_installed:
        print("✅ All dependencies are installed!")
        print()
        print("You can now run the server:")
        print("  cd backend && python main.py")
    else:
        print("❌ Some dependencies are missing!")
        print()
        print("Install them with:")
        print("  pip install -r requirements.txt")
    
    print("=" * 60)
    
    return 0 if all_installed else 1

if __name__ == "__main__":
    sys.exit(main())
