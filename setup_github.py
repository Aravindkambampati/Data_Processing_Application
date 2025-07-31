#!/usr/bin/env python3
"""
GitHub Setup Script for Data Processing Application
This script helps set up Git and push the project to GitHub.
"""

import os
import subprocess
import sys
import webbrowser
from pathlib import Path

def check_git_installed():
    """Check if Git is installed"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git is installed!")
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def install_git_instructions():
    """Provide instructions to install Git"""
    print("\n📦 Git Installation Required")
    print("=" * 50)
    print("Git is not installed on your system.")
    print("\nTo install Git:")
    print("1. Download Git from: https://git-scm.com/download/win")
    print("2. Run the installer with default settings")
    print("3. Restart your terminal/command prompt")
    print("4. Run this script again")
    
    # Open Git download page
    try:
        webbrowser.open("https://git-scm.com/download/win")
        print("\n🌐 Opening Git download page...")
    except:
        print("\n📋 Please manually visit: https://git-scm.com/download/win")

def setup_git_repo():
    """Set up Git repository"""
    print("\n🔧 Setting up Git repository...")
    
    # Initialize Git repository
    try:
        subprocess.run(['git', 'init'], check=True)
        print("✅ Git repository initialized")
    except subprocess.CalledProcessError:
        print("❌ Failed to initialize Git repository")
        return False
    
    # Add all files
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ Files added to Git")
    except subprocess.CalledProcessError:
        print("❌ Failed to add files to Git")
        return False
    
    # Create initial commit
    try:
        subprocess.run(['git', 'commit', '-m', 'Initial commit: Advanced Data Processor'], check=True)
        print("✅ Initial commit created")
    except subprocess.CalledProcessError:
        print("❌ Failed to create initial commit")
        return False
    
    return True

def create_github_repo_instructions():
    """Provide instructions to create GitHub repository"""
    print("\n📋 GitHub Repository Setup")
    print("=" * 50)
    print("To push to GitHub:")
    print("\n1. Go to GitHub: https://github.com")
    print("2. Click 'New repository'")
    print("3. Name it: 'data-processing-app'")
    print("4. Make it Public or Private")
    print("5. Don't initialize with README (we already have one)")
    print("6. Click 'Create repository'")
    print("7. Copy the repository URL")
    print("8. Run the push commands shown below")
    
    # Open GitHub
    try:
        webbrowser.open("https://github.com")
        print("\n🌐 Opening GitHub...")
    except:
        print("\n📋 Please manually visit: https://github.com")

def show_push_commands():
    """Show the commands to push to GitHub"""
    print("\n🚀 Push Commands")
    print("=" * 50)
    print("After creating the GitHub repository, run these commands:")
    print("\n# Add the remote repository (replace with your URL)")
    print("git remote add origin https://github.com/YOUR_USERNAME/data-processing-app.git")
    print("\n# Push to GitHub")
    print("git branch -M main")
    print("git push -u origin main")
    print("\n# For future updates")
    print("git add .")
    print("git commit -m 'Update: description of changes'")
    print("git push")

def create_gitignore():
    """Create .gitignore file if it doesn't exist"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyQt5
*.ui
*.qrc

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Application specific
*.log
temp/
cache/
"""
    
    gitignore_path = Path('.gitignore')
    if not gitignore_path.exists():
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore file")

def main():
    """Main function"""
    print("🚀 GitHub Setup for Data Processing Application")
    print("=" * 60)
    
    # Check if Git is installed
    if not check_git_installed():
        install_git_instructions()
        return
    
    # Create .gitignore
    create_gitignore()
    
    # Set up Git repository
    if setup_git_repo():
        print("\n✅ Git repository setup complete!")
        
        # Show GitHub instructions
        create_github_repo_instructions()
        
        # Show push commands
        show_push_commands()
        
        print("\n🎉 Setup complete! Follow the instructions above to push to GitHub.")
    else:
        print("\n❌ Failed to set up Git repository")

if __name__ == "__main__":
    main() 