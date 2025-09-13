"""
MCP tool for fetching climate data from Open Meteo API.
"""
import requests
from typing import Dict, Any


def fetch_climate_data(location: str) -> Dict[str, Any]:
    """
    MCP tool to fetch climate data from Open Meteo API.
    
    Args:
        location: Location name for climate data (currently supports "New York")
        
    Returns:
        JSON response with temperature and weather data or error information
    """
    try:
        # For this implementation, we'll use New York coordinates as specified
        # In a production system, you'd want to add geocoding for other locations
        location_coords = {
            "new york": {"lat": 40.71, "lon": -74.01},
            "newyork": {"lat": 40.71, "lon": -74.01},
            "ny": {"lat": 40.71, "lon": -74.01}
        }
        
        location_key = location.lower().replace(" ", "")
        
        if location_key not in location_coords:
            # Default to New York if location not found
            coords = location_coords["newyork"]
        else:
            coords = location_coords[location_key]
        
        lat, lon = coords["lat"], coords["lon"]
        
        # Fetch current weather and 7-day forecast
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"current_weather=true&"
            f"daily=temperature_2m_max,temperature_2m_min,precipitation_sum&"
            f"timezone=auto"
        )
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Validate response structure
        if not isinstance(data, dict):
            return {
                "error": "Invalid response format from Open Meteo API",
                "current_weather": {},
                "daily": {}
            }
            
        return data
        
    except requests.exceptions.Timeout:
        return {
            "error": "Request timeout while fetching climate data",
            "current_weather": {},
            "daily": {}
        }
    except requests.exceptions.ConnectionError:
        return {
            "error": "Connection error while accessing Open Meteo API",
            "current_weather": {},
            "daily": {}
        }
    except requests.exceptions.HTTPError as e:
        status_code = getattr(e.response, 'status_code', 'Unknown') if e.response else 'Unknown'
        reason = getattr(e.response, 'reason', 'Unknown') if e.response else 'Unknown'
        return {
            "error": f"HTTP error {status_code}: {reason}",
            "current_weather": {},
            "daily": {}
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Request failed: {str(e)}",
            "current_weather": {},
            "daily": {}
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "current_weather": {},
            "daily": {}
        }