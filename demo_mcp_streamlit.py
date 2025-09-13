"""
Demo script showing MCP tools integration with Streamlit app.
"""
from tools.species_tool import fetch_species
from tools.climate_tool import fetch_climate_data
from streamlit_utils import fetch_species_data_streamlit

def demo_mcp_integration():
    """Demonstrate how MCP tools are integrated into the Streamlit app."""
    
    print("🐾 Wildlife Insight Agent - MCP Integration Demo")
    print("=" * 50)
    
    # Show direct MCP tool usage
    print("\n1. 🔧 Direct MCP Tool Usage:")
    print("   Using fetch_species MCP tool directly...")
    
    tiger_data = fetch_species("tiger")
    print(f"   ✅ Found {tiger_data.get('count', 0)} tiger species via MCP tool")
    
    if tiger_data.get('results'):
        first_species = tiger_data['results'][0]
        print(f"   📋 First result: {first_species.get('scientificName', 'N/A')}")
    
    print("\n   Using fetch_climate_data MCP tool directly...")
    climate_data = fetch_climate_data("New York")
    
    if 'current_weather' in climate_data:
        temp = climate_data['current_weather'].get('temperature', 'N/A')
        wind = climate_data['current_weather'].get('windspeed', 'N/A')
        print(f"   🌤️ New York weather: {temp}°C, Wind: {wind} km/h")
    
    # Show Streamlit integration
    print("\n2. 🌐 Streamlit Integration:")
    print("   Streamlit app uses the same MCP tools...")
    
    streamlit_data = fetch_species_data_streamlit("elephant")
    print(f"   ✅ Streamlit found {streamlit_data.get('count', 0)} elephant species")
    
    # Show how it works in the full pipeline
    print("\n3. 🤖 CrewAI Pipeline Integration:")
    print("   The Streamlit app now:")
    print("   • Uses fetch_species MCP tool in Task 1")
    print("   • Uses fetch_climate_data MCP tool in Task 2") 
    print("   • Combines both datasets in Task 3 (Analysis)")
    print("   • Generates reports with climate context in Task 4")
    
    print("\n4. 🚀 How to Run:")
    print("   Command Line: python main.py")
    print("   Streamlit Web: streamlit run app.py")
    print("   Both now use the same MCP tools!")
    
    print("\n" + "=" * 50)
    print("✅ MCP Integration Complete!")

if __name__ == "__main__":
    demo_mcp_integration()