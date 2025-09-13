#!/usr/bin/env python3
"""
Streamlit utilities for Wildlife Insight Agent

This module provides Streamlit-optimized versions of the main functions
with better error handling and progress tracking for web interface.
"""

import requests
import json
import streamlit as st
from crewai import Agent, Task, Crew, LLM
import sys
from io import StringIO
import contextlib
from tools.species_tool import fetch_species
from tools.climate_tool import fetch_climate_data

def fetch_species_data_streamlit(query: str) -> dict:
    """
    Fetch species data using MCP species tool (Streamlit version).
    
    Args:
        query (str): Species name or search term
        
    Returns:
        dict: JSON response from GBIF API via MCP tool or error information
    """
    return fetch_species(query)

@contextlib.contextmanager
def capture_output():
    """Context manager to capture stdout and stderr"""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    stdout_capture = StringIO()
    stderr_capture = StringIO()
    try:
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        yield stdout_capture, stderr_capture
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

def run_wildlife_analysis_streamlit(species_query: str, progress_callback=None):
    """
    Run the wildlife analysis pipeline for Streamlit (with progress tracking).
    
    Args:
        species_query (str): The species to search for
        progress_callback: Optional callback function for progress updates
    
    Returns:
        tuple: (result, logs) where result is the final report and logs are captured output
    """
    
    # Configure Gemini LLM
    gemini_llm = LLM(
        model="gemini/gemini-1.5-flash",
        api_key="AIzaSyBaWl8qVr0EFMOMlWNFycPRJyf4xAsmsWI"
    )
    
    if progress_callback:
        progress_callback(20, "Initializing AI agents...")
    
    # Define the Research Agent
    research_agent = Agent(
        role="Wildlife Researcher",
        goal="Fetch species data from the GBIF API",
        backstory="""You are an expert wildlife researcher with deep knowledge of 
        biodiversity databases and scientific data sources. You specialize in retrieving 
        accurate species information from the Global Biodiversity Information Facility (GBIF) 
        and ensuring data quality for conservation research.""",
        verbose=False,  # Reduced verbosity for Streamlit
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
        verbose=False,  # Reduced verbosity for Streamlit
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
        verbose=False,  # Reduced verbosity for Streamlit
        allow_delegation=False,
        llm=gemini_llm
    )
    
    if progress_callback:
        progress_callback(40, "Fetching species data...")
    
    # Get species data using MCP tool
    species_data = fetch_species(species_query)
    
    # Get climate data using MCP tool
    climate_data = fetch_climate_data("New York")
    
    # Register MCP tools with the research agent
    research_agent.tools = [fetch_species, fetch_climate_data]
    
    # Define Task 1: Fetch Species Data using MCP tool
    research_task = Task(
        description=f"""Use the fetch_species MCP tool to gather comprehensive data about '{species_query}'. 
        Call the tool with '{species_query}' as the species name parameter. 
        Return the complete JSON response including species information, scientific classification, 
        and any available occurrence data.""",
        agent=research_agent,
        expected_output=f"Complete species data from GBIF API via MCP tool including scientific names, classification, and occurrence information for {species_query}"
    )
    
    # Define Task 2: Fetch Climate Data using MCP tool
    climate_task = Task(
        description="""Use the fetch_climate_data MCP tool to gather current weather and 
        climate information for New York. Call the tool with 'New York' as the location parameter. 
        Return the complete JSON response including current weather conditions and forecast data.""",
        agent=research_agent,
        expected_output="Complete climate data including current weather conditions, temperature forecasts, and precipitation data for New York"
    )
    
    # Define Task 3: Analysis
    analysis_task = Task(
        description=f"""Analyze the species and climate data from the previous tasks. Extract 
        key information including:
        - Total number of {species_query} species found
        - Scientific names and conservation status
        - Distribution patterns and occurrence counts
        - Climate context from New York weather data
        - Potential correlations between environmental conditions and species habitat
        
        Provide structured insights combining both datasets for conservation reporting.""",
        agent=analysis_agent,
        expected_output=f"""Structured analysis including {species_query} species counts, conservation status, 
        climate context, and key findings about species distribution with environmental correlations""",
        context=[research_task, climate_task]
    )
    
    # Define Task 4: Report Generation
    report_task = Task(
        description=f"""Create a comprehensive, beginner-friendly report based on the analysis insights. 
        The report should:
        - Use simple, non-technical language suitable for students and conservation enthusiasts
        - Explain key findings about {species_query} species with climate context
        - Highlight conservation concerns and environmental relationships
        - Include interesting facts about distribution and habitat preferences
        - Connect species data with climate information from New York
        
        Focus on educational value and conservation awareness with environmental context.""",
        agent=report_agent,
        expected_output=f"""A clear, beginner-friendly report about {species_query} species that 
        includes conservation status, climate context, distribution insights, and environmental 
        correlations in simple language""",
        context=[analysis_task]
    )
    
    if progress_callback:
        progress_callback(60, "Creating AI crew...")
    
    # Create the crew with all four tasks
    crew = Crew(
        agents=[research_agent, analysis_agent, report_agent],
        tasks=[research_task, climate_task, analysis_task, report_task],
        verbose=False  # Reduced verbosity for Streamlit
    )
    
    try:
        if progress_callback:
            progress_callback(80, "Executing analysis pipeline...")
        
        # Capture output during crew execution
        with capture_output() as (stdout_capture, stderr_capture):
            result = crew.kickoff()
        
        # Get captured logs
        logs = {
            'stdout': stdout_capture.getvalue(),
            'stderr': stderr_capture.getvalue()
        }
        
        if progress_callback:
            progress_callback(100, "Analysis complete!")
        
        return result, logs, species_data, climate_data
        
    except Exception as e:
        error_msg = f"Error executing crew: {str(e)}"
        if progress_callback:
            progress_callback(0, f"Error: {error_msg}")
        return None, {'error': error_msg}, species_data, climate_data