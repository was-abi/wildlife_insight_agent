"""
Example of how to use the MCP tools directly.
"""
from tools.species_tool import fetch_species
from tools.climate_tool import fetch_climate_data
import json

def demo_species_tool():
    """Demonstrate species tool usage."""
    print("=== Species Tool Demo ===")
    
    # Fetch tiger data
    tiger_data = fetch_species("tiger")
    print(f"Tiger species found: {tiger_data.get('count', 0)}")
    
    if 'results' in tiger_data and tiger_data['results']:
        first_result = tiger_data['results'][0]
        print(f"Scientific name: {first_result.get('scientificName', 'N/A')}")
        print(f"Kingdom: {first_result.get('kingdom', 'N/A')}")
        print(f"Class: {first_result.get('class', 'N/A')}")
    
    # Try other species
    elephant_data = fetch_species("elephant")
    print(f"\nElephant species found: {elephant_data.get('count', 0)}")
    
    return tiger_data, elephant_data

def demo_climate_tool():
    """Demonstrate climate tool usage."""
    print("\n=== Climate Tool Demo ===")
    
    # Fetch New York climate data
    ny_climate = fetch_climate_data("New York")
    
    if 'current_weather' in ny_climate:
        current = ny_climate['current_weather']
        print(f"Current temperature: {current.get('temperature', 'N/A')}°C")
        print(f"Wind speed: {current.get('windspeed', 'N/A')} km/h")
    
    if 'daily' in ny_climate and 'temperature_2m_max' in ny_climate['daily']:
        max_temps = ny_climate['daily']['temperature_2m_max'][:3]  # First 3 days
        print(f"Next 3 days max temps: {max_temps}")
    
    return ny_climate

if __name__ == "__main__":
    # Run demos
    species_data = demo_species_tool()
    climate_data = demo_climate_tool()
    
    print("\n=== Raw Data Examples ===")
    print("Species data keys:", list(species_data[0].keys()))
    print("Climate data keys:", list(climate_data.keys()))