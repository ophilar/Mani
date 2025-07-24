#!/usr/bin/env python3
"""
Setup script for SLAM Manim visualizations.

This script helps users set up the environment and run their first animation.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_uv_installed():
    """Check if uv is installed."""
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_uv():
    """Install uv if not already installed."""
    print("Installing uv...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "uv"
        ], check=True)
        print("✅ uv installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install uv. Please install it manually:")
        print("   pip install uv")
        return False


def setup_environment():
    """Set up the Python environment using uv."""
    print("Setting up Python environment...")
    try:
        subprocess.run(["uv", "sync"], check=True)
        print("✅ Environment set up successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to set up environment.")
        return False


def run_first_animation():
    """Run the first animation to test the setup."""
    print("Running first animation (SO3 Rotation)...")
    try:
        subprocess.run([
            "uv", "run", "manim", "-pql", "so3_visualization.py", 
            "SO3RotationVisualization"
        ], check=True)
        print("✅ First animation completed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to run animation. Check your setup.")
        return False


def main():
    """Main setup function."""
    print("🚀 SLAM Manim Visualizations Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check and install uv
    if not check_uv_installed():
        print("uv not found. Installing...")
        if not install_uv():
            sys.exit(1)
    else:
        print("✅ uv is already installed.")
    
    # Set up environment
    if not setup_environment():
        sys.exit(1)
    
    # Run first animation
    print("\n🎬 Testing the setup with a simple animation...")
    if not run_first_animation():
        print("\n⚠️  Animation failed, but environment is set up.")
        print("   You can try running animations manually:")
        print("   uv run manim -pql so3_visualization.py SO3RotationVisualization")
    else:
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Explore the available animations in the README.md")
        print("2. Try different quality settings: -pql, -pqm, -pqh")
        print("3. Customize parameters in config.py")
        print("4. Create your own animations!")


if __name__ == "__main__":
    main() 