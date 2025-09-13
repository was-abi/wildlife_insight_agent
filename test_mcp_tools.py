"""
Unit tests for MCP tools with mocked API responses.
"""
import unittest
from unittest.mock import patch, Mock
import json
import requests
from tools.species_tool import fetch_species
from tools.climate_tool import fetch_climate_data


class TestSpeciesTool(unittest.TestCase):
    """Test cases for the species MCP tool."""
    
    @patch('tools.species_tool.requests.get')
    def test_fetch_species_success(self, mock_get):
        """Test successful species data fetch."""
        # Mock successful GBIF API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {
                    "key": 2435099,
                    "scientificName": "Panthera tigris",
                    "canonicalName": "Panthera tigris",
                    "rank": "SPECIES",
                    "status": "ACCEPTED",
                    "confidence": 100,
                    "kingdom": "Animalia",
                    "phylum": "Chordata",
                    "class": "Mammalia",
                    "order": "Carnivora",
                    "family": "Felidae",
                    "genus": "Panthera"
                }
            ],
            "count": 1,
            "endOfRecords": True
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = fetch_species("tiger")
        
        self.assertIn("results", result)
        self.assertEqual(len(result["results"]), 1)
        self.assertEqual(result["results"][0]["scientificName"], "Panthera tigris")
        mock_get.assert_called_once_with("https://api.gbif.org/v1/species/search?q=tiger", timeout=30)
    
    @patch('tools.species_tool.requests.get')
    def test_fetch_species_connection_error(self, mock_get):
        """Test handling of connection errors."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        result = fetch_species("tiger")
        
        self.assertIn("error", result)
        self.assertIn("Connection error", result["error"])
        self.assertEqual(result["results"], [])
        self.assertEqual(result["count"], 0)
    
    @patch('tools.species_tool.requests.get')
    def test_fetch_species_timeout(self, mock_get):
        """Test handling of timeout errors."""
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        result = fetch_species("tiger")
        
        self.assertIn("error", result)
        self.assertIn("Request timeout", result["error"])
        self.assertEqual(result["results"], [])
    
    @patch('tools.species_tool.requests.get')
    def test_fetch_species_http_error(self, mock_get):
        """Test handling of HTTP errors."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_get.return_value = mock_response
        
        result = fetch_species("invalid_species")
        
        self.assertIn("error", result)
        self.assertIn("HTTP error", result["error"])


class TestClimateTool(unittest.TestCase):
    """Test cases for the climate MCP tool."""
    
    @patch('tools.climate_tool.requests.get')
    def test_fetch_climate_data_success(self, mock_get):
        """Test successful climate data fetch."""
        # Mock successful Open Meteo API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "latitude": 40.71,
            "longitude": -74.01,
            "current_weather": {
                "temperature": 15.2,
                "windspeed": 10.5,
                "winddirection": 180,
                "weathercode": 1,
                "time": "2024-01-15T12:00"
            },
            "daily": {
                "time": ["2024-01-15", "2024-01-16", "2024-01-17"],
                "temperature_2m_max": [18.5, 20.1, 16.8],
                "temperature_2m_min": [8.2, 10.5, 7.9],
                "precipitation_sum": [0.0, 2.5, 0.1]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = fetch_climate_data("New York")
        
        self.assertIn("current_weather", result)
        self.assertIn("daily", result)
        self.assertEqual(result["current_weather"]["temperature"], 15.2)
        self.assertEqual(len(result["daily"]["time"]), 3)
    
    @patch('tools.climate_tool.requests.get')
    def test_fetch_climate_data_connection_error(self, mock_get):
        """Test handling of connection errors."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        result = fetch_climate_data("New York")
        
        self.assertIn("error", result)
        self.assertIn("Connection error", result["error"])
        self.assertEqual(result["current_weather"], {})
        self.assertEqual(result["daily"], {})
    
    @patch('tools.climate_tool.requests.get')
    def test_fetch_climate_data_timeout(self, mock_get):
        """Test handling of timeout errors."""
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        result = fetch_climate_data("New York")
        
        self.assertIn("error", result)
        self.assertIn("Request timeout", result["error"])
    
    def test_fetch_climate_data_unknown_location(self):
        """Test handling of unknown locations (should default to New York)."""
        with patch('tools.climate_tool.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {"latitude": 40.71, "longitude": -74.01}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            result = fetch_climate_data("Unknown City")
            
            # Should still make a request (defaulting to New York coordinates)
            mock_get.assert_called_once()
            call_args = mock_get.call_args[0][0]
            self.assertIn("latitude=40.71", call_args)
            self.assertIn("longitude=-74.01", call_args)


if __name__ == '__main__':
    unittest.main()