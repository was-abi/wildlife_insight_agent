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

def fetch_species_data_streamlit(query: str) -> dict:
    """
    Fetch species data from the GBIF API (Streamlit version).
    
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
        return data
        
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        return {
            "error": error_msg,
            "results": [],
            "count": 0
        }
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON response: {str(e)}"
        return {
            "error": error_msg,
            "results": [],
            "count": 0
        }

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
    
    # Get species data
    species_data = fetch_species_data_streamlit(species_query)
    
    # Define Task 1: Research
    research_task = Task(
        description=f"""Retrieve information about '{species_query}' from the GBIF API. 
        Here is the data from the GBIF API: {species_data}
        
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
    
    if progress_callback:
        progress_callback(60, "Creating AI crew...")
    
    # Create the crew
    crew = Crew(
        agents=[research_agent, analysis_agent, report_agent],
        tasks=[research_task, analysis_task, report_task],
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
        
        return result, logs, species_data
        
    except Exception as e:
        error_msg = f"Error executing crew: {str(e)}"
        if progress_callback:
            progress_callback(0, f"Error: {error_msg}")
        return None, {'error': error_msg}, species_data