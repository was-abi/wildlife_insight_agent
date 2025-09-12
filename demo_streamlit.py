#!/usr/bin/env python3
"""
Demo script to test Streamlit components without running the full server.
"""

from streamlit_utils import fetch_species_data_streamlit, run_wildlife_analysis_streamlit
import time

def test_streamlit_functions():
    """Test the Streamlit utility functions"""
    print("🧪 Testing Streamlit utility functions...")
    
    # Test 1: API data fetching
    print("\n1. Testing GBIF API data fetching...")
    species_data = fetch_species_data_streamlit("tiger")
    print(f"   ✓ Found {species_data.get('count', 0)} tiger-related species")
    
    # Test 2: Progress callback simulation
    print("\n2. Testing progress callback...")
    def mock_progress(progress, message):
        print(f"   Progress: {progress}% - {message}")
    
    print("\n3. Testing streamlined analysis (this may take a moment)...")
    try:
        result, logs, final_data = run_wildlife_analysis_streamlit(
            "pug", 
            progress_callback=mock_progress
        )
        
        if result:
            print("   ✅ Analysis completed successfully!")
            print(f"   📊 Final species count: {final_data.get('count', 0)}")
            print(f"   📝 Report length: {len(str(result))} characters")
        else:
            print("   ❌ Analysis failed")
            
    except Exception as e:
        print(f"   ❌ Error during analysis: {e}")
    
    print("\n🎉 Streamlit utility testing complete!")

if __name__ == "__main__":
    test_streamlit_functions()