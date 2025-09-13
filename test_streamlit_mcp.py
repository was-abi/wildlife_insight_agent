"""
Test script to verify MCP tools are properly integrated with Streamlit utilities.
"""
from streamlit_utils import fetch_species_data_streamlit, run_wildlife_analysis_streamlit
from tools.species_tool import fetch_species as mcp_fetch_species
from tools.climate_tool import fetch_climate_data as mcp_fetch_climate

def test_mcp_integration():
    """Test that Streamlit utilities use MCP tools correctly."""
    
    print("=== Testing MCP Integration with Streamlit ===")
    
    # Test 1: Direct MCP tool usage
    print("\n1. Testing direct MCP tools...")
    species_result = mcp_fetch_species("tiger")
    climate_result = mcp_fetch_climate("New York")
    
    print(f"Species tool returned {species_result.get('count', 0)} tiger species")
    print(f"Climate tool returned temperature: {climate_result.get('current_weather', {}).get('temperature', 'N/A')}°C")
    
    # Test 2: Streamlit wrapper using MCP tools
    print("\n2. Testing Streamlit wrapper with MCP tools...")
    streamlit_species_result = fetch_species_data_streamlit("tiger")
    
    print(f"Streamlit wrapper returned {streamlit_species_result.get('count', 0)} tiger species")
    
    # Test 3: Verify they return the same data
    print("\n3. Verifying consistency...")
    if species_result.get('count') == streamlit_species_result.get('count'):
        print("✅ Streamlit wrapper correctly uses MCP species tool")
    else:
        print("❌ Streamlit wrapper not using MCP species tool correctly")
    
    # Test 4: Check if tools are properly imported
    print("\n4. Checking imports...")
    try:
        import streamlit_utils
        # Check if the MCP tools are available in the module
        if hasattr(streamlit_utils, 'fetch_species') and hasattr(streamlit_utils, 'fetch_climate_data'):
            print("✅ MCP tools successfully imported in streamlit_utils")
        else:
            print("❌ MCP tools not found in streamlit_utils")
    except ImportError as e:
        print(f"❌ Import error: {e}")
    
    print("\n=== MCP Integration Test Complete ===")

if __name__ == "__main__":
    test_mcp_integration()