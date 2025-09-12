#!/usr/bin/env python3
"""
Wildlife Insight Agent - Web Launcher

Simple launcher script for the Streamlit web interface.
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit web application"""
    try:
        print("🌐 Starting Wildlife Insight Agent Web Interface...")
        print("🚀 Launching Streamlit server...")
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down Wildlife Insight Agent...")
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")
        print("💡 Make sure Streamlit is installed: pip install streamlit")

if __name__ == "__main__":
    main()