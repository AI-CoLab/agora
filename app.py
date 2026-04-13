"""
Australian Government Organisations Register (AGOR) Explorer

An interactive Streamlit application for exploring the structure
of the Australian Government.

Data source: https://data.gov.au/data/dataset/australian-government-organisations-register
"""

import streamlit as st

from data.loader import load_agor_data
from components.overview import render_overview
from components.treemap import render_treemap
from components.sunburst import render_sunburst
from components.explorer import render_explorer
from components.network import render_network
from components.org_detail import render_org_detail

st.set_page_config(
    page_title="Australian Government Organisations",
    page_icon="\U0001f3db\ufe0f",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Minimal branding CSS ---
st.markdown(
    """
    <style>
        .main .block-container { padding-top: 1rem; }
        h1 { color: #002E5D; }
        .stMetric label { font-size: 0.9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Load data ---
df = load_agor_data()

# --- Sidebar ---
with st.sidebar:
    st.title("AGOR Explorer")
    st.markdown("Explore the structure of the Australian Government")
    st.divider()

    view = st.radio(
        "Select view",
        [
            "Overview",
            "Portfolio Treemap",
            "Sunburst Chart",
            "Organisation Explorer",
            "Relationship Network",
            "Organisation Lookup",
        ],
        index=0,
    )

    st.divider()
    st.caption(f"**{len(df):,}** organisations loaded")
    st.caption("Source: [data.gov.au](https://data.gov.au/data/dataset/australian-government-organisations-register)")

# --- Main content ---
st.title("Australian Government Organisations Register")

if view == "Overview":
    st.markdown(
        "A high-level summary of the structure and composition "
        "of the Australian Government."
    )
    render_overview(df)

elif view == "Portfolio Treemap":
    st.subheader("Government Structure by Portfolio")
    st.markdown(
        "Each rectangle represents a grouping of organisations. "
        "The size shows how many organisations belong to each group."
    )
    render_treemap(df)

elif view == "Sunburst Chart":
    st.subheader("Hierarchical View")
    st.markdown(
        "A radial view of the government structure. "
        "The centre represents all government, with rings expanding outward."
    )
    render_sunburst(df)

elif view == "Organisation Explorer":
    st.subheader("Search & Filter Organisations")
    st.markdown(
        "Find specific organisations by searching or filtering. "
        "Download the results as a CSV file."
    )
    render_explorer(df)

elif view == "Relationship Network":
    st.subheader("Organisation Relationships")
    st.markdown(
        "Interactive graph showing parent-child relationships "
        "between organisations within a portfolio. Drag nodes to rearrange."
    )
    render_network(df)

elif view == "Organisation Lookup":
    st.subheader("Organisation Details")
    st.markdown(
        "Select an organisation to view its full details, "
        "parent chain, and sub-bodies."
    )
    render_org_detail(df)
