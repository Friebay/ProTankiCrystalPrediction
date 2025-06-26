#!/usr/bin/env python3
"""
Setup script for ProTanki Crystal Prediction
This script checks for dependencies and helps with installation.
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_requirements():
    """Install required packages from requirements.txt."""
    try:
        print("📦 Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt not found!")
        return False

def check_tesseract():
    """Check if Tesseract OCR is installed."""
    tesseract_path = r'C:\Users\zabit\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    if os.path.exists(tesseract_path):
        print("✅ Tesseract OCR found!")
        return True
    else:
        print("❌ Tesseract OCR not found!")
        print("Please download and install Tesseract from:")
        print("https://github.com/UB-Mannheim/tesseract/wiki")
        print(f"Expected path: {tesseract_path}")
        return False

def check_required_files():
    """Check if required files exist."""
    required_files = [
        "diamond.png",
        "ready.mp3", 
        "screenshot.mp3"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            missing_files.append(file)
    
    return len(missing_files) == 0

def main():
    """Main setup function."""
    print("ProTanki Crystal Prediction - Setup Check")
    print("=" * 50)
    
    all_good = True
    
    # Check Python version
    if not check_python_version():
        all_good = False
    
    print()
    
    # Install requirements
    if not install_requirements():
        all_good = False
    
    print()
    
    # Check Tesseract
    if not check_tesseract():
        all_good = False
    
    print()
    
    # Check required files
    if not check_required_files():
        all_good = False
    
    print()
    print("=" * 50)
    
    if all_good:
        print("🎉 Setup complete! You can now run the program with:")
        print("python run_program.py")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
    
    return all_good

if __name__ == "__main__":
    main()
