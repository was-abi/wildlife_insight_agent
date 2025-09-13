#!/usr/bin/env python3
"""
Wildlife Insight Agent - Streamlit Web Interface

A beautiful web interface for the CrewAI-based multi-agent system that researches,
analyzes, and reports on wildlife species data from the GBIF API.
"""

import streamlit as st
import requests
import json
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
from streamlit_utils import run_wildlife_analysis_streamlit, fetch_species_data_streamlit

# Page configuration
st.set_page_config(
    page_title="Wildlife Insight Agent",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .species-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        border-left: 4px solid #2E8B57;
        margin: 1rem 0;
        min-height: 150px;
    }
    
    .metric-card h3 {
        color: #2E8B57 !important;
        margin-bottom: 1rem !important;
        font-size: 1.2rem !important;
    }
    
    .metric-card p {
        color: #333 !important;
        line-height: 1.6 !important;
        font-size: 0.95rem !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(46,139,87,0.3);
    }
    
    .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Ensure text visibility */
    .stMarkdown p {
        color: #333 !important;
    }
    
    .stMarkdown h2 {
        color: #2E8B57 !important;
        margin-bottom: 1rem !important;
    }
    
    .stMarkdown h3 {
        color: #2E8B57 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Welcome section specific styling */
    .welcome-section {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🐾 Wildlife Insight Agent</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; color: #666;">
        <p style="font-size: 1.2rem;">Discover wildlife species data through AI-powered research and analysis</p>
        <p>Powered by CrewAI, GBIF API, and Gemini LLM</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 Species Selection")
        
        # Predefined species options
        species_options = {
            "🐅 Tiger": "tiger",
            "🐋 Whale": "whale", 
            "🐘 Elephant": "elephant",
            "🐶 Pug": "pug"
        }
        
        # Species selection
        selected_option = st.selectbox(
            "Choose a species to analyze:",
            ["Select a species..."] + list(species_options.keys()) + ["🔍 Custom species"]
        )
        
        # Custom species input
        custom_species = ""
        if selected_option == "🔍 Custom species":
            custom_species = st.text_input(
                "Enter species name:",
                placeholder="e.g., polar bear, dolphin, eagle"
            )
        
        # Analysis button
        analyze_button = st.button("🚀 Start Analysis", type="primary")
        
        # Information section
        st.markdown("---")
        st.markdown("## 📊 About")
        st.markdown("""
        This tool uses three AI agents:
        - **🔬 Research Agent**: Fetches data from GBIF
        - **📈 Analysis Agent**: Processes and analyzes data  
        - **📝 Report Agent**: Creates beginner-friendly reports
        """)
        
        st.markdown("## 🌍 Data Source")
        st.markdown("""
        Data is retrieved from the [Global Biodiversity Information Facility (GBIF)](https://www.gbif.org/), 
        the world's largest network of biodiversity data.
        """)
    
    # Main content area
    if analyze_button:
        # Determine species to analyze
        if selected_option == "🔍 Custom species" and custom_species:
            species_query = custom_species.lower().strip()
        elif selected_option in species_options:
            species_query = species_options[selected_option]
        else:
            st.error("Please select a species or enter a custom species name.")
            return
        
        # Display selected species
        st.markdown(f"""
        <div class="species-card">
            <h2>🔍 Analyzing: {species_query.title()}</h2>
            <p>Starting comprehensive wildlife analysis...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create columns for metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Initialize metrics
        with col1:
            species_count_placeholder = st.empty()
        with col2:
            status_placeholder = st.empty()
        with col3:
            progress_placeholder = st.empty()
        with col4:
            time_placeholder = st.empty()
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        start_time = time.time()
        
        try:
            # Step 1: Fetch initial data
            status_text.text("🔍 Fetching species data from GBIF...")
            progress_bar.progress(10)
            
            # Get basic species data for metrics
            species_data = fetch_species_data_streamlit(species_query)
            species_count = species_data.get('count', 0)
            
            # Update metrics
            with col1:
                st.metric("Species Found", f"{species_count:,}")
            with col2:
                status_label = "✅ Retrieved" if species_count > 0 else "⚠️ Limited"
                st.metric("Status", status_label)
            with col3:
                st.metric("Progress", "10%")
            
            progress_bar.progress(30)
            status_text.text("🤖 Initializing AI agents...")
            
            # Step 2: Run the full analysis
            progress_bar.progress(50)
            status_text.text("🧠 AI agents analyzing data...")
            
            # Progress callback function
            def update_progress(progress, message):
                progress_bar.progress(progress)
                status_text.text(message)
            
            # Capture the analysis output
            with st.spinner("Running CrewAI analysis pipeline..."):
                result, logs, final_species_data = run_wildlife_analysis_streamlit(
                    species_query, 
                    progress_callback=update_progress
                )
            
            progress_bar.progress(90)
            status_text.text("📝 Generating final report...")
            
            # Calculate elapsed time
            elapsed_time = time.time() - start_time
            with col4:
                st.metric("Analysis Time", f"{elapsed_time:.1f}s")
            with col3:
                st.metric("Progress", "100%")
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
            # Display results
            if result:
                st.markdown("---")
                st.markdown("## 📋 Wildlife Insight Report")
                
                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["📖 Full Report", "📊 Data Insights", "🔬 Technical Details"])
                
                with tab1:
                    st.markdown("### 🐾 Conservation Report")
                    st.markdown(result)
                
                with tab2:
                    # Create visualizations if we have data
                    if species_count > 0:
                        # Species count chart
                        fig = go.Figure(data=go.Bar(
                            x=[species_query.title()],
                            y=[species_count],
                            marker_color='#2E8B57'
                        ))
                        fig.update_layout(
                            title=f"Species Records Found for '{species_query.title()}'",
                            xaxis_title="Species Query",
                            yaxis_title="Number of Records",
                            showlegend=False
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Sample data visualization
                        if 'results' in species_data and species_data['results']:
                            # Create a simple taxonomy breakdown
                            kingdoms = {}
                            for result in species_data['results'][:10]:  # First 10 results
                                kingdom = result.get('kingdom', 'Unknown')
                                kingdoms[kingdom] = kingdoms.get(kingdom, 0) + 1
                            
                            if kingdoms:
                                fig_pie = px.pie(
                                    values=list(kingdoms.values()),
                                    names=list(kingdoms.keys()),
                                    title=f"Taxonomic Kingdoms for '{species_query.title()}' (Sample)"
                                )
                                st.plotly_chart(fig_pie, use_container_width=True)
                    else:
                        st.info("No occurrence data available for visualization.")
                
                with tab3:
                    st.markdown("### 🔬 Technical Analysis Details")
                    
                    # API Response Summary
                    st.markdown("#### GBIF API Response")
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Total Records", species_data.get('count', 0))
                    with col_b:
                        st.metric("Results Returned", len(species_data.get('results', [])))
                    with col_c:
                        st.metric("End of Records", "Yes" if species_data.get('endOfRecords', False) else "No")
                    
                    # Sample data
                    if 'results' in species_data and species_data['results']:
                        st.markdown("#### Sample Species Data")
                        sample_data = []
                        for i, result in enumerate(species_data['results'][:5]):
                            sample_data.append({
                                'Scientific Name': result.get('scientificName', 'N/A'),
                                'Kingdom': result.get('kingdom', 'N/A'),
                                'Phylum': result.get('phylum', 'N/A'),
                                'Class': result.get('class', 'N/A'),
                                'Rank': result.get('rank', 'N/A'),
                                'Status': result.get('taxonomicStatus', 'N/A')
                            })
                        
                        df = pd.DataFrame(sample_data)
                        st.dataframe(df, use_container_width=True)
                    
                    # Analysis metadata
                    st.markdown("#### Analysis Metadata")
                    metadata = {
                        'Query': species_query,
                        'Analysis Time': f"{elapsed_time:.2f} seconds",
                        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'API Endpoint': f"https://api.gbif.org/v1/species/search?q={species_query}",
                        'AI Model': "Gemini 1.5 Flash",
                        'Framework': "CrewAI"
                    }
                    
                    for key, value in metadata.items():
                        st.text(f"{key}: {value}")
            
            else:
                st.error("❌ Analysis failed. Please try again or contact support.")
        
        except Exception as e:
            st.error(f"❌ An error occurred during analysis: {str(e)}")
            progress_bar.progress(0)
            status_text.text("❌ Analysis failed")
    
    else:
        # Welcome screen
        st.markdown("## 🌟 Welcome to Wildlife Insight Agent")
        st.markdown("### Discover the fascinating world of wildlife through AI-powered research")
        
        # Feature highlights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #2E8B57; margin-bottom: 1rem;">🔬 AI-Powered Research</h3>
                <p style="color: #333; line-height: 1.6;">Three specialized AI agents work together to research, analyze, and report on wildlife species data.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #2E8B57; margin-bottom: 1rem;">🌍 Global Data</h3>
                <p style="color: #333; line-height: 1.6;">Access to millions of species records from the Global Biodiversity Information Facility (GBIF).</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: #2E8B57; margin-bottom: 1rem;">📚 Educational Reports</h3>
                <p style="color: #333; line-height: 1.6;">Beginner-friendly conservation reports that make complex data accessible to everyone.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Sample species showcase
        st.markdown("## 🐾 Featured Species")
        st.markdown("**Explore these popular species to get started:**")
        
        showcase_col1, showcase_col2, showcase_col3, showcase_col4 = st.columns(4)
        
        with showcase_col1:
            try:
                st.image("https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=300&h=200&fit=crop", caption="🐅 Tigers")
            except:
                st.markdown("🐅 **Tigers**")
            st.markdown("**Explore tiger species and conservation status worldwide.**")
        
        with showcase_col2:
            try:
                st.image("https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=200&fit=crop", caption="🐋 Whales")
            except:
                st.markdown("🐋 **Whales**")
            st.markdown("**Discover whale species and marine conservation efforts.**")
        
        with showcase_col3:
            try:
                st.image("https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=300&h=200&fit=crop", caption="🐘 Elephants")
            except:
                st.markdown("🐘 **Elephants**")
            st.markdown("**Learn about elephant populations and habitat protection.**")
        
        with showcase_col4:
            try:
                st.image("https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=300&h=200&fit=crop", caption="🐶 Pugs")
            except:
                st.markdown("🐶 **Pugs**")
            st.markdown("**Investigate pug-related species across different kingdoms.**")
        
        # Instructions
        st.markdown("## 🚀 How to Use")
        st.markdown("**Follow these simple steps to analyze wildlife species:**")
        
        instruction_col1, instruction_col2 = st.columns(2)
        
        with instruction_col1:
            st.markdown("""
            **Step 1: Choose Your Species**
            - Select from predefined options (Tiger, Whale, Elephant, Pug)
            - Or enter a custom species name
            
            **Step 2: Start Analysis**
            - Click the 'Start Analysis' button
            - Watch the AI agents work together
            """)
        
        with instruction_col2:
            st.markdown("""
            **Step 3: Explore Results**
            - Read the full conservation report
            - View data visualizations and insights
            - Check technical details and metadata
            
            **Step 4: Learn & Discover**
            - Understand conservation status
            - Explore biodiversity patterns
            """)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; margin-top: 2rem;">
            <p>Built with ❤️ using Streamlit, CrewAI, and Gemini LLM</p>
            <p>Data provided by the Global Biodiversity Information Facility (GBIF)</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()