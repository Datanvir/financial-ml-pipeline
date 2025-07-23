#!/usr/bin/env python3
"""
Financial ML Pipeline Project Setup Script

This script creates the necessary folder structure, requirements.txt file,
and Python virtual environment for a financial machine learning pipeline project.
"""

import os
import subprocess
import sys
from pathlib import Path


def create_directories():
    """Create project directories if they don't exist."""
    directories = ['data', 'notebooks', 'src', 'reports']
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory already exists: {directory}")


def create_requirements_file():
    """Create requirements.txt file with necessary packages."""
    requirements_path = Path('requirements.txt')
    
    packages = [
        'pandas',
        'numpy',
        'scikit-learn',
        'matplotlib',
        'jupyter',
        'mlfinlab',
        'yfinance'
    ]
    
    if not requirements_path.exists():
        with open(requirements_path, 'w') as f:
            for package in packages:
                f.write(f"{package}\n")
        print("✓ Created requirements.txt with financial ML packages")
    else:
        print("✓ requirements.txt already exists")


def create_virtual_environment():
    """Create Python virtual environment."""
    venv_path = Path('.venv')
    
    if not venv_path.exists():
        try:
            print("Creating Python virtual environment...")
            subprocess.run([sys.executable, '-m', 'venv', '.venv'], check=True)
            print("✓ Virtual environment created successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to create virtual environment: {e}")
            return False
    else:
        print("✓ Virtual environment already exists")
    
    return True


def print_activation_instructions():
    """Print instructions for activating the virtual environment."""
    print("\n" + "="*60)
    print("VIRTUAL ENVIRONMENT ACTIVATION INSTRUCTIONS")
    print("="*60)
    
    print("\n🖥️  On Windows:")
    print("   .venv\\Scripts\\activate")
    
    print("\n🍎  On macOS/Linux:")
    print("   source .venv/bin/activate")
    
    print("\n📦 After activation, install dependencies with:")
    print("   pip install -r requirements.txt")
    
    print("\n🚀 To deactivate the environment:")
    print("   deactivate")
    print("="*60)


def main():
    """Main function to set up the project."""
    print("Setting up Financial ML Pipeline Project...")
    print("-" * 50)
    
    # Create directories
    create_directories()
    
    # Create requirements.txt
    create_requirements_file()
    
    # Create virtual environment
    venv_created = create_virtual_environment()
    
    # Print activation instructions
    if venv_created:
        print_activation_instructions()
    
    print("\n🎉 Project scaffold created!")


if __name__ == "__main__":
    main()
