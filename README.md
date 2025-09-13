# Wildlife Species + Climate Insight Agent (MCP Edition)

A Python-based multi-agent system using CrewAI + MCP (Model Context Protocol) to automatically research, analyze, and report on wildlife species and climate data from multiple APIs.

## Overview

The Wildlife Insight Agent uses three specialized AI agents working through four tasks with MCP tools:
- **Research Agent**: Uses MCP tools to fetch species data from GBIF API and climate data from Open Meteo API
- **Analysis Agent**: Analyzes combined species and climate data to identify conservation insights and environmental correlations
- **Report Agent**: Generates beginner-friendly reports combining biodiversity and climate information

## How It Works

- Research Agent calls two MCP tools:
  * `fetch_species` → queries GBIF for species data
  * `fetch_climate_data` → queries Open Meteo API for location-specific climate data
- Analysis Agent merges both datasets into insights
- Report Agent summarizes into a human-readable report with climate context

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the project:
   ```bash
   python main.py
   ```

## Example Output

```
=== Final Report ===
Tiger species (Panthera tigris) is classified as endangered.
Climate data for New York shows max temperatures of 28°C this week.
The combination highlights how climate and biodiversity trends are linked.
```

## Usage Options

### Interactive Mode (Default)
Run the application and choose from the menu:
```bash
python main.py
```
Available species:
- 🐅 Tiger
- 🐋 Whale  
- 🐘 Elephant
- 🐶 Pug
- 🔍 Custom species
- 🚀 Run all species

### Command Line Mode
Analyze a specific species directly:
```bash
python main.py tiger
python main.py whale
python main.py elephant
python main.py pug
python main.py "polar bear"
```

## Features

- **Multi-species support**: Tigers, whales, elephants, pugs, and custom species
- **Interactive menu system** for easy species selection
- **Command-line interface** for direct species queries
- **Beautiful web interface** built with Streamlit
- **Real-time progress tracking** with visual indicators
- **Interactive data visualizations** using Plotly
- **Batch processing** to analyze all species at once
- **Automated wildlife species data retrieval** from GBIF
- **Multi-agent analysis pipeline** using CrewAI with Gemini LLM
- **Beginner-friendly conservation reports** in accessible language
- **Comprehensive error handling** for API failures and data issues
- **Multiple report formats**: Full report, data insights, and technical details

## API Data Source

This application uses the [Global Biodiversity Information Facility (GBIF)](https://www.gbif.org/) API, which provides access to biodiversity data from around the world.

## Project Structure

```
wildlife_insight_agent/
├── main.py              # Main application entry point with MCP tool registration
├── requirements.txt     # Python dependencies (including mcp)
├── README.md           # Project documentation
├── tools/              # MCP tools directory
│   ├── species_tool.py # GBIF species data MCP tool
│   └── climate_tool.py # Climate data MCP tool
└── .kiro/              # Kiro configuration and specs
```

## Example Output

The system generates comprehensive reports for each species that include:
- **Species occurrence counts** and diversity metrics
- **Conservation status information** and threat assessments  
- **Distribution trends and patterns** across different regions
- **Key findings** presented in accessible, beginner-friendly language
- **Educational insights** about biodiversity and conservation importance

### Sample Species Coverage
- **Tigers**: Various tiger-named species including insects, frogs, and marine life
- **Whales**: Marine mammals and whale-related species from global databases
- **Elephants**: Elephant species and elephant-named organisms
- **Pugs**: Dog breeds and pug-related species entries

## Web Interface

The Wildlife Insight Agent includes a beautiful Streamlit web interface with:

- **Interactive species selection** with real-time progress tracking
- **Visual data exploration** with charts and graphs using Plotly
- **Multiple report formats**: Full reports, data insights, and technical details
- **Responsive design** that works on desktop, tablet, and mobile
- **Educational content** making wildlife research accessible to everyone

See [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) for detailed web interface documentation.

## 🚀 Live Demo

**Try the live app:** [Wildlife Insight Agent on Render](https://wildlife-insight-agent.onrender.com) *(Deploy following the guide below)*

## 🌐 Deployment

### Render (Recommended)
Deploy to Render for a live, shareable web application:

1. **Fork this repository** to your GitHub account
2. **Sign up at [render.com](https://render.com)** (free tier available)
3. **Connect your GitHub repository** to Render
4. **Follow the detailed guide:** [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

The app works in **demo mode** without API keys, or with **full AI functionality** when you add your Gemini API key as an environment variable.

### Local Development
```bash
# Clone the repository
git clone https://github.com/yourusername/wildlife-insight-agent
cd wildlife-insight-agent

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

## Requirements

- Python 3.8+
- Internet connection for GBIF API access
- Dependencies listed in requirements.txt
- Modern web browser for Streamlit interface
- Optional: Gemini API key for full AI functionality