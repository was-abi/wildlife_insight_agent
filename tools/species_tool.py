"""
MCP tool for fetching species data from GBIF API.
"""
import requests
from typing import Dict, Any


def fetch_species(species_name: str) -> Dict[str, Any]:
    """
    MCP tool to fetch species data from GBIF API.
    
    Args:
        species_name: Name of species to search for
        
    Returns:
        JSON response from GBIF API or error information
    """
    try:
        url = f"https://api.gbif.org/v1/species/search?q={species_name}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Validate response structure
        if not isinstance(data, dict):
            return {
                "error": "Invalid response format from GBIF API",
                "results": [],
                "count": 0
            }
            
        return data
        
    except requests.exceptions.Timeout:
        return {
            "error": "Request timeout while fetching species data",
            "results": [],
            "count": 0
        }
    except requests.exceptions.ConnectionError:
        return {
            "error": "Connection error while accessing GBIF API",
            "results": [],
            "count": 0
        }
    except requests.exceptions.HTTPError as e:
        status_code = getattr(e.response, 'status_code', 'Unknown') if e.response else 'Unknown'
        reason = getattr(e.response, 'reason', 'Unknown') if e.response else 'Unknown'
        return {
            "error": f"HTTP error {status_code}: {reason}",
            "results": [],
            "count": 0
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Request failed: {str(e)}",
            "results": [],
            "count": 0
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "results": [],
            "count": 0
        }