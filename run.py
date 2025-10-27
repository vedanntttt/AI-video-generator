#!/usr/bin/env python3
"""
Run script for AI Animated Video Generator
This script starts the Streamlit application with proper configuration
"""

import subprocess
import sys
import os

def main():
    """Start the Streamlit application"""
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Not running in a virtual environment")
        print("💡 Consider running: python -m venv venv && source venv/bin/activate")
        print()
    
    # Check if required packages are installed
    try:
        import streamlit
        import moviepy
        import edge_tts
        print("✅ All required packages are available")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return 1
    
    # Create necessary directories
    try:
        import utils
        utils.create_directories()
        print("✅ Directories created successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not create directories: {e}")
    
    # Check FFmpeg availability
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✅ FFmpeg is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Warning: FFmpeg not found. Video processing may fail.")
        print("💡 Install FFmpeg: https://ffmpeg.org/download.html")
    
    print("\n🚀 Starting AI Animated Video Generator...")
    print("📱 The app will open in your default browser")
    print("🔗 Manual URL: http://localhost:8501")
    print("\n" + "="*50)
    
    # Start Streamlit
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port', '8501',
            '--server.address', '0.0.0.0',
            '--browser.gatherUsageStats', 'false'
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())