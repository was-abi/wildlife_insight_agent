"""
Wildlife Insight Agent - Main application entry point.
Uses CrewAI framework with MCP tools for wildlife research and reporting.
"""
import sys
import json
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from tools.species_tool import fetch_species
from tools.climate_tool import fetch_climate_data


class SpeciesTool(BaseTool):
    """CrewAI-compatible wrapper for the species MCP tool."""
    name: str = "fetch_species"
    description: str = "Fetch species data from GBIF API using MCP tool. Input should be a species name."
    
    def _run(self, species_name: str) -> str:
        """Execute the species tool and return JSON string."""
        result = fetch_species(species_name)
        return json.dumps(result, indent=2)


class ClimateTool(BaseTool):
    """CrewAI-compatible wrapper for the climate MCP tool."""
    name: str = "fetch_climate_data"
    description: str = "Fetch climate data from Open Meteo API using MCP tool. Input should be a location name."
    
    def _run(self, location: str) -> str:
        """Execute the climate tool and return JSON string."""
        result = fetch_climate_data(location)
        return json.dumps(result, indent=2)


def create_research_agent():
    """Create the Research Agent for data fetching."""
    return Agent(
        role="Wildlife Researcher",
        goal="Fetch comprehensive species and climate data using MCP tools",
        backstory=(
            "You are an expert wildlife researcher with deep knowledge of "
            "biodiversity databases and climate data sources. You specialize "
            "in using standardized MCP tools to gather accurate scientific "
            "information from the Global Biodiversity Information Facility "
            "and climate APIs."
        ),
        verbose=True,
        allow_delegation=False
    )


def create_analysis_agent():
    """Create the Analysis Agent for data processing."""
    return Agent(
        role="Data Analyst",
        goal="Analyze species and climate data to identify conservation insights",
        backstory=(
            "You are a skilled data analyst specializing in biodiversity and "
            "environmental data. You excel at finding patterns in species "
            "distribution, identifying endangered status indicators, and "
            "correlating wildlife data with climate conditions to generate "
            "meaningful conservation insights."
        ),
        verbose=True,
        allow_delegation=False
    )


def create_report_agent():
    """Create the Report Agent for generating user-friendly reports."""
    return Agent(
        role="Report Writer",
        goal="Create beginner-friendly reports about wildlife and climate findings",
        backstory=(
            "You are an experienced science communicator who specializes in "
            "translating complex biodiversity and climate research into "
            "accessible, engaging reports for students and conservationists. "
            "You use simple language while maintaining scientific accuracy."
        ),
        verbose=True,
        allow_delegation=False
    )


def create_tasks(research_agent, analysis_agent, report_agent):
    """Create the four sequential tasks for the wildlife research pipeline."""
    
    # Task 1: Fetch species data using MCP tool
    task1 = Task(
        description=(
            "Use the fetch_species MCP tool to gather comprehensive data about tigers. "
            "Call the tool with 'tiger' as the species name parameter. "
            "Return the complete JSON response including species information, "
            "scientific classification, and any available occurrence data."
        ),
        agent=research_agent,
        expected_output=(
            "Complete species data from GBIF API including scientific name, "
            "classification hierarchy, and occurrence information for tigers."
        )
    )
    
    # Task 2: Fetch climate data using MCP tool  
    task2 = Task(
        description=(
            "Use the fetch_climate_data MCP tool to gather current weather and "
            "climate information for New York. Call the tool with 'New York' "
            "as the location parameter. Return the complete JSON response "
            "including current weather conditions and forecast data."
        ),
        agent=research_agent,
        expected_output=(
            "Complete climate data including current weather conditions, "
            "temperature forecasts, and precipitation data for New York."
        )
    )
    
    # Task 3: Analyze combined data
    task3 = Task(
        description=(
            "Analyze the species and climate data from the previous tasks. "
            "Extract key information including: species occurrence counts, "
            "conservation status indicators, distribution patterns, "
            "temperature trends, and potential correlations between "
            "climate conditions and species habitat preferences. "
            "Focus on conservation insights and environmental relationships."
        ),
        agent=analysis_agent,
        expected_output=(
            "Structured analysis including species occurrence statistics, "
            "conservation status assessment, climate pattern summary, "
            "and identified correlations between environmental conditions "
            "and species distribution."
        ),
        context=[task1, task2]
    )
    
    # Task 4: Generate final report
    task4 = Task(
        description=(
            "Create a comprehensive, beginner-friendly report summarizing "
            "the wildlife and climate findings. Use simple, non-technical "
            "language suitable for students and conservation enthusiasts. "
            "Include key conservation insights, climate context, and "
            "explain the importance of the findings for wildlife protection."
        ),
        agent=report_agent,
        expected_output=(
            "A clear, accessible report in simple language that explains "
            "the tiger species information, climate conditions, conservation "
            "status, and the relationship between environmental factors "
            "and wildlife conservation."
        ),
        context=[task3]
    )
    
    return [task1, task2, task3, task4]


def main():
    """Main function to execute the wildlife insight agent pipeline."""
    try:
        print("Initializing Wildlife Insight Agent...")
        print("Setting up MCP tools and CrewAI agents...")
        
        # Create agents
        research_agent = create_research_agent()
        analysis_agent = create_analysis_agent()
        report_agent = create_report_agent()
        
        # Create tasks
        tasks = create_tasks(research_agent, analysis_agent, report_agent)
        
        # Create CrewAI-compatible tool instances
        species_tool = SpeciesTool()
        climate_tool = ClimateTool()
        
        # Register MCP tools with agents
        research_agent.tools = [species_tool, climate_tool]
        
        # Create and configure the crew
        crew = Crew(
            agents=[research_agent, analysis_agent, report_agent],
            tasks=tasks,
            verbose=True
        )
        
        print("\nStarting wildlife research pipeline...")
        print("=" * 50)
        
        # Execute the crew
        result = crew.kickoff()
        
        # Display final report
        print("\n" + "=" * 50)
        print("=== Final Report ===")
        print("=" * 50)
        print(result)
        
        return result
        
    except Exception as e:
        print(f"Error executing wildlife insight agent: {str(e)}")
        return None


if __name__ == "__main__":
    main()