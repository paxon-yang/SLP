#!/usr/bin/env python3
"""
Automated GitHub Deployment Script for Document Viewer
Handles image compression and GitHub repository setup
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(f"   {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"   {e.stderr.strip()}")
        return False

def check_requirements():
    """Check if all required dependencies are available"""
    print("Checking requirements...")
    
    # Check Git
    if not shutil.which('git'):
        print("Git is not installed or not in PATH")
        print("   Please install Git first: https://git-scm.com/")
        return False
    
    # Check Python and Pillow
    try:
        from PIL import Image
        print("Python and Pillow are available")
    except ImportError:
        print("Pillow not found. Installing...")
        if not run_command("pip install Pillow", "Installing Pillow"):
            print("Failed to install Pillow")
            return False
    
    return True

def compress_images():
    """Run the image compression script"""
    print("\nCompressing images...")
    
    if not os.path.exists("compress_images.py"):
        print("compress_images.py not found")
        return False
    
    return run_command("python compress_images.py", "Running image compression")

def setup_git_repository():
    """Initialize git repository if not already done"""
    print("\nSetting up Git repository...")
    
    if os.path.exists(".git"):
        print("Git repository already exists")
        return True
    
    commands = [
        ("git init", "Initializing Git repository"),
        ("git add .", "Adding files to Git"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def get_user_input():
    """Get repository information from user"""
    print("\nRepository Setup")
    print("=" * 40)
    
    while True:
        username = input("Enter your GitHub username: ").strip()
        if username:
            break
        print("Username cannot be empty")
    
    while True:
        repo_name = input("Enter repository name: ").strip()
        if repo_name:
            break
        print("Repository name cannot be empty")
    
    commit_message = input("Enter commit message (or press Enter for default): ").strip()
    if not commit_message:
        commit_message = "Initial commit: Document viewer with compressed images"
    
    return username, repo_name, commit_message

def commit_and_push(username, repo_name, commit_message):
    """Commit changes and push to GitHub"""
    print(f"\nDeploying to GitHub...")
    
    commands = [
        (f'git commit -m "{commit_message}"', "Committing changes"),
        ("git branch -M main", "Setting main branch"),
        (f"git remote add origin https://github.com/{username}/{repo_name}.git", "Adding remote origin"),
        ("git push -u origin main", "Pushing to GitHub"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            if "remote origin already exists" in command:
                # Try to update the remote URL instead
                update_command = f"git remote set-url origin https://github.com/{username}/{repo_name}.git"
                if not run_command(update_command, "Updating remote origin"):
                    return False
                # Try push again
                if not run_command("git push -u origin main", "Pushing to GitHub"):
                    return False
            else:
                return False
    
    return True

def display_final_instructions(username, repo_name):
    """Display final setup instructions"""
    print("\n" + "=" * 60)
    print("DEPLOYMENT COMPLETE!")
    print("=" * 60)
    print(f"Your repository: https://github.com/{username}/{repo_name}")
    print(f"Your website: https://github.com/{username}/{repo_name}")
    print("\nNext Steps:")
    print("1. Go to your GitHub repository")
    print("2. Click on 'Settings' tab")
    print("3. Scroll down to 'Pages' section")
    print("4. Under 'Source', select 'GitHub Actions'")
    print("5. Wait a few minutes for deployment")
    print(f"6. Access your site at: https://{username}.github.io/{repo_name}")
    print("\nYour document viewer is now live on the web!")

def main():
    """Main deployment function"""
    print("Document Viewer - GitHub Deployment Tool")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Compress images
    if not compress_images():
        print("Image compression failed")
        sys.exit(1)
    
    # Setup git
    if not setup_git_repository():
        print("Git setup failed")
        sys.exit(1)
    
    # Get user input
    username, repo_name, commit_message = get_user_input()
    
    # Confirm deployment
    print(f"\nDeployment Summary:")
    print(f"   GitHub Username: {username}")
    print(f"   Repository Name: {repo_name}")
    print(f"   Commit Message: {commit_message}")
    print(f"   Website URL: https://{username}.github.io/{repo_name}")
    
    confirm = input("\nProceed with deployment? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Deployment cancelled")
        sys.exit(0)
    
    # Commit and push
    if not commit_and_push(username, repo_name, commit_message):
        print("Deployment failed")
        sys.exit(1)
    
    # Display final instructions
    display_final_instructions(username, repo_name)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDeployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1) 