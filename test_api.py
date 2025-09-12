#!/usr/bin/env python3
"""
Simple test script to verify GBIF API connectivity and response structure.
"""

from main import fetch_species_data
import json


def test_api_client():
    """Test the GBIF API client with different scenarios."""
    print("🧪 Testing GBIF API Client")
    print("=" * 40)
    
    # Test 1: Valid species query
    print("\n1. Testing with 'tiger' query...")
    tiger_data = fetch_species_data("tiger")
    
    if "error" not in tiger_data:
        print(f"   ✓ Success: Found {tiger_data.get('count', 0)} results")
        if tiger_data.get('results'):
            first_result = tiger_data['results'][0]
            print(f"   ✓ First result: {first_result.get('scientificName', 'N/A')}")
    else:
        print(f"   ✗ Error: {tiger_data['error']}")
    
    # Test 2: Empty query
    print("\n2. Testing with empty query...")
    empty_data = fetch_species_data("")
    print(f"   Results count: {empty_data.get('count', 0)}")
    
    # Test 3: Scientific name query
    print("\n3. Testing with scientific name 'Panthera tigris'...")
    scientific_data = fetch_species_data("Panthera tigris")
    
    if "error" not in scientific_data:
        print(f"   ✓ Success: Found {scientific_data.get('count', 0)} results")
    else:
        print(f"   ✗ Error: {scientific_data['error']}")
    
    print("\n" + "=" * 40)
    print("API client testing complete!")


if __name__ == "__main__":
    test_api_client()