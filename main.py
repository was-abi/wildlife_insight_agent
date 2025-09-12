#!/usr/bin/env python3
"""
Wildlife Insight Agent - A CrewAI-based multi-agent system for wildlife research and reporting.

This application uses three specialized AI agents to fetch, analyze, and report on
wildlife species data from the Global Biodiversity Information Facility (GBIF) API.
"""

import requests
import json
import os
import sys
from crewai import Agent, Task, Crew, LLM


def fetch_species_data(query: str) -> dict:
    """
    Fetch species data from the GBIF API.
    
    Args:
        query (str): Species name or search term
        
    Returns:
        dict: JSON response from GBIF API or error information
    """
    try:
        url = f"https://api.gbif.org/v1/species/search?q={query}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"✓ Successfully fetched data for '{query}' - Found {data.get('count', 0)} results")
        return data
        
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        print(f"✗ {error_msg}")
        return {
            "error": error_msg,
            "results": [],
            "count": 0
        }
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON response: {str(e)}"
        print(f"✗ {error_msg}")
        return {
            "error": error_msg,
            "results": [],
            "count": 0
        }


def run_wildlife_analysis(species_query: str):
    """
    Run the wildlife analysis pipeline for a specific species query.
    
    Args:
        species_query (str): The species to search for (e.g., 'tiger', 'whale', 'elephant', 'pug')
    
    Returns:
        str: The final report or None if failed
    """
    print(f"🐾 Starting Wildlife Insight Agent for '{species_query}'...")
    print("=" * 60)
    
    # Configure Gemini LLM
    gemini_llm = LLM(
        model="gemini/gemini-1.5-flash",
        api_key="AIzaSyBaWl8qVr0EFMOMlWNFycPRJyf4xAsmsWI"
    )
    
    # Define the Research Agent
    research_agent = Agent(
        role="Wildlife Researcher",
        goal="Fetch species data from the GBIF API",
        backstory="""You are an expert wildlife researcher with deep knowledge of 
        biodiversity databases and scientific data sources. You specialize in retrieving 
        accurate species information from the Global Biodiversity Information Facility (GBIF) 
        and ensuring data quality for conservation research.""",
        verbose=True,
        allow_delegation=False,
        llm=gemini_llm
    )
    
    # Define the Analysis Agent
    analysis_agent = Agent(
        role="Data Analyst",
        goal="Analyze species occurrence data and extract key insights",
        backstory="""You are a skilled data analyst specializing in biodiversity and 
        conservation science. You excel at finding patterns in species occurrence data, 
        identifying endangered species, and extracting meaningful trends from complex 
        biological datasets for conservation purposes.""",
        verbose=True,
        allow_delegation=False,
        llm=gemini_llm
    )
    
    # Define the Report Agent
    report_agent = Agent(
        role="Report Writer",
        goal="Summarize the analysis in simple, beginner-friendly language",
        backstory="""You are an experienced science communicator who specializes in 
        making complex wildlife and conservation data accessible to students and the 
        general public. You excel at writing clear, engaging reports that help people 
        understand important conservation issues.""",
        verbose=True,
        allow_delegation=False,
        llm=gemini_llm
    )
    
    # Define Task 1: Research
    research_task = Task(
        description=f"""Retrieve information about '{species_query}' from the GBIF API. 
        Here is the data from the GBIF API: {fetch_species_data(species_query)}
        
        Analyze this data and provide a summary of the species information found, 
        including scientific names, occurrence counts, and any conservation-related details.""",
        agent=research_agent,
        expected_output=f"Summary of {species_query} species data from GBIF API including key species information and occurrence details"
    )
    
    # Define Task 2: Analysis
    analysis_task = Task(
        description="""Analyze the species data received from the research task. Extract 
        key information including:
        - Total number of species found
        - Scientific names and common names
        - Conservation status indicators
        - Distribution patterns and occurrence counts
        - Any endangered or threatened species information
        
        Provide structured insights that can be used for conservation reporting.""",
        agent=analysis_agent,
        expected_output=f"""Structured analysis including species counts, conservation status, 
        and key findings about {species_query} species distribution and conservation concerns"""
    )
    
    # Define Task 3: Report Generation
    report_task = Task(
        description=f"""Create a beginner-friendly report based on the analysis insights. 
        The report should:
        - Use simple, non-technical language
        - Explain key findings about {species_query} species
        - Highlight conservation concerns and status
        - Include interesting facts about distribution
        - Be accessible to students and general public
        
        Focus on educational value and conservation awareness.""",
        agent=report_agent,
        expected_output=f"""A clear, beginner-friendly report about {species_query} species that 
        includes conservation status, distribution insights, and key findings in simple language"""
    )
    
    # Create the crew
    crew = Crew(
        agents=[research_agent, analysis_agent, report_agent],
        tasks=[research_task, analysis_task, report_task],
        verbose=True
    )
    
    try:
        print("🚀 Executing CrewAI pipeline...")
        print("-" * 30)
        
        # Execute the crew
        result = crew.kickoff()
        
        print("\n" + "=" * 60)
        print(f"📋 FINAL WILDLIFE INSIGHT REPORT - {species_query.upper()}")
        print("=" * 60)
        print(result)
        print("=" * 60)
        
        return result
        
    except Exception as e:
        print(f"❌ Error executing crew: {str(e)}")
        return None


def main():
    """
    Main function with command-line interface for species selection.
    """
    # Available species options
    available_species = {
        "1": "tiger",
        "2": "whale", 
        "3": "elephant",
        "4": "pug"
    }
    
    # Check if species was provided as command line argument
    if len(sys.argv) > 1:
        species_query = sys.argv[1].lower()
        print(f"🔍 Running analysis for: {species_query}")
        return run_wildlife_analysis(species_query)
    
    # Interactive menu
    print("🌍 Welcome to the Wildlife Insight Agent!")
    print("=" * 50)
    print("Choose a species to analyze:")
    print("1. 🐅 Tiger")
    print("2. 🐋 Whale") 
    print("3. 🐘 Elephant")
    print("4. 🐶 Pug")
    print("5. 🔍 Custom species (enter your own)")
    print("6. 🚀 Run all species")
    print("=" * 50)
    
    choice = input("Enter your choice (1-6): ").strip()
    
    if choice in available_species:
        species_query = available_species[choice]
        return run_wildlife_analysis(species_query)
    elif choice == "5":
        species_query = input("Enter the species name to search for: ").strip()
        if species_query:
            return run_wildlife_analysis(species_query)
        else:
            print("❌ No species name provided!")
            return None
    elif choice == "6":
        print("🚀 Running analysis for all available species...")
        results = {}
        for species in available_species.values():
            print(f"\n{'='*20} ANALYZING {species.upper()} {'='*20}")
            results[species] = run_wildlife_analysis(species)
            print(f"\n{'='*20} COMPLETED {species.upper()} {'='*20}")
        
        # Summary
        print("\n" + "🌟" * 60)
        print("📊 SUMMARY OF ALL SPECIES ANALYSES")
        print("🌟" * 60)
        for species, result in results.items():
            status = "✅ Success" if result else "❌ Failed"
            print(f"{species.capitalize()}: {status}")
        print("🌟" * 60)
        
        return results
    else:
        print("❌ Invalid choice! Please run the program again.")
        return None


if __name__ == "__main__":
    main()