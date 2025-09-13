#!/usr/bin/env python3
"""
Simple test to verify the welcome section displays correctly
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Wildlife Insight Agent - Test",
    page_icon="🐾",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🐾 Wildlife Insight Agent</h1>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem; color: #666;">
    <p style="font-size: 1.2rem;">Discover wildlife species data through AI-powered research and analysis</p>
    <p>Powered by CrewAI, GBIF API, and Gemini LLM</p>
</div>
""", unsafe_allow_html=True)

# Welcome screen
st.markdown("## 🌟 Welcome to Wildlife Insight Agent")
st.markdown("### Discover the fascinating world of wildlife through AI-powered research")

# Test if basic text shows up
st.write("**This is a test to ensure text visibility works properly.**")
st.success("✅ If you can see this message, the basic text rendering is working!")

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

# Alternative text display methods
st.markdown("---")
st.markdown("## 🧪 Text Visibility Tests")

st.markdown("**Method 1: Regular markdown**")
st.markdown("This text should be visible using regular markdown.")

st.markdown("**Method 2: st.write()**")
st.write("This text should be visible using st.write().")

st.markdown("**Method 3: HTML with inline styles**")
st.markdown('<p style="color: #333; font-size: 1rem;">This text uses HTML with inline styles.</p>', unsafe_allow_html=True)

st.markdown("**Method 4: Streamlit text elements**")
st.text("This is using st.text() - should always be visible.")

st.info("ℹ️ This is an info box - should be visible with blue background.")
st.success("✅ This is a success box - should be visible with green background.")
st.warning("⚠️ This is a warning box - should be visible with yellow background.")

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