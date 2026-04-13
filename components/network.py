"""Interactive network graph of parent-child organisation relationships."""

import pandas as pd
import streamlit as st

from utils.constants import CLASSIFICATION_COLORS

try:
    import networkx as nx
    from pyvis.network import Network

    HAS_NETWORK_LIBS = True
except ImportError:
    HAS_NETWORK_LIBS = False


def render_network(df: pd.DataFrame):
    """Render an interactive network graph for a selected portfolio."""
    if not HAS_NETWORK_LIBS:
        st.error("Network visualisation requires networkx and pyvis. Install them with: pip install networkx pyvis")
        return

    portfolios = sorted(df["Portfolio"].dropna().unique())
    selected_portfolio = st.selectbox(
        "Select a portfolio to visualise",
        portfolios,
        key="network_portfolio",
    )

    subset = df[df["Portfolio"] == selected_portfolio].copy()

    if subset.empty:
        st.warning("No organisations found in this portfolio.")
        return

    st.markdown(f"**{len(subset)}** organisations in this portfolio")

    # Build directed graph
    G = nx.DiGraph()

    for _, row in subset.iterrows():
        title = row["Title"]
        classification = row.get("Classification", "Unknown")
        type_of_body = row.get("Type of Body", "Unknown")
        is_portfolio_dept = str(row.get("Portfolio Dept?", "")).lower() == "yes"

        G.add_node(
            title,
            label=_shorten_label(title),
            title=f"{title}\n{classification}\n{type_of_body}",
            color=CLASSIFICATION_COLORS.get(classification, "#cccccc"),
            size=30 if is_portfolio_dept else 18,
            shape="dot",
        )

    # Add edges for parent relationships
    for _, row in subset.iterrows():
        parent = row.get("Parent Organisation")
        if pd.notna(parent) and parent != "None" and parent in G.nodes:
            G.add_edge(parent, row["Title"])

    # Also add parent nodes that might be outside this portfolio
    for _, row in subset.iterrows():
        parent = row.get("Parent Organisation")
        if pd.notna(parent) and parent != "None" and parent not in G.nodes:
            # Look up the parent in the full dataset
            parent_rows = df[df["Title"] == parent]
            if not parent_rows.empty:
                parent_row = parent_rows.iloc[0]
                G.add_node(
                    parent,
                    label=_shorten_label(parent),
                    title=f"{parent}\n(External: {parent_row.get('Portfolio', 'Unknown')})",
                    color="#E0E0E0",
                    size=20,
                    shape="diamond",
                )
                G.add_edge(parent, row["Title"])

    # Render with pyvis
    net = Network(
        height="650px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
        font_color="#333333",
    )
    net.from_nx(G)
    net.set_options("""{
        "physics": {
            "barnesHut": {
                "gravitationalConstant": -4000,
                "centralGravity": 0.3,
                "springLength": 120,
                "springConstant": 0.04
            },
            "stabilization": {"iterations": 150}
        },
        "edges": {
            "arrows": {"to": {"enabled": true, "scaleFactor": 0.5}},
            "color": {"color": "#888888"},
            "smooth": {"type": "cubicBezier"}
        },
        "interaction": {
            "hover": true,
            "tooltipDelay": 100,
            "zoomView": true,
            "dragView": true
        },
        "nodes": {
            "font": {"size": 12, "face": "Arial"}
        }
    }""")

    html = net.generate_html()
    st.components.v1.html(html, height=680, scrolling=True)

    # Legend
    st.markdown("**Legend:**")
    legend_cols = st.columns(len(CLASSIFICATION_COLORS) + 1)
    for i, (cls, color) in enumerate(CLASSIFICATION_COLORS.items()):
        with legend_cols[i]:
            st.markdown(
                f'<span style="color:{color}; font-size:20px;">&#9679;</span> {cls}',
                unsafe_allow_html=True,
            )
    with legend_cols[-1]:
        st.markdown(
            '<span style="color:#E0E0E0; font-size:20px;">&#9670;</span> External Parent',
            unsafe_allow_html=True,
        )


def _shorten_label(title: str, max_len: int = 35) -> str:
    """Shorten a title for display as a node label."""
    if len(title) <= max_len:
        return title
    return title[: max_len - 3] + "..."
