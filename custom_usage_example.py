"""
Example of customizing the wildlife insight agent with different species and locations.
"""
from tools.species_tool import fetch_species
from tools.climate_tool import fetch_climate_data

def analyze_custom_species_and_location(species_name, location="New York"):
    """
    Analyze any species with climate data from any supported location.
    
    Args:
        species_name: Name of species to research
        location: Location for climate data (currently supports New York)
    """
    print(f"=== Analyzing {species_name.title()} with {location} Climate ===")
    
    # Fetch species data
    print(f"Fetching {species_name} data from GBIF...")
    species_data = fetch_species(species_name)
    
    if 'error' in species_data:
        print(f"Species data error: {species_data['error']}")
    else:
        print(f"Found {species_data.get('count', 0)} {species_name} species")
        
        # Show first few results
        if species_data.get('results'):
            for i, result in enumerate(species_data['results'][:3]):
                print(f"  {i+1}. {result.get('scientificName', 'Unknown')}")
    
    # Fetch climate data
    print(f"\nFetching climate data for {location}...")
    climate_data = fetch_climate_data(location)
    
    if 'error' in climate_data:
        print(f"Climate data error: {climate_data['error']}")
    else:
        if 'current_weather' in climate_data:
            temp = climate_data['current_weather'].get('temperature', 'N/A')
            print(f"Current temperature in {location}: {temp}°C")
    
    return species_data, climate_data

def main():
    """Run custom analysis examples."""
    
    # Example 1: Elephants
    print("Example 1: Elephants")
    elephant_data, ny_climate = analyze_custom_species_and_location("elephant")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Whales
    print("Example 2: Whales")
    whale_data, ny_climate2 = analyze_custom_species_and_location("whale")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Pandas
    print("Example 3: Pandas")
    panda_data, ny_climate3 = analyze_custom_species_and_location("panda")

if __name__ == "__main__":
    main()