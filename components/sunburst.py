"""Sunburst hierarchy chart using Plotly."""

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.constants import CLASSIFICATION_COLORS


def render_sunburst(df: pd.DataFrame):
    """Render an interactive sunburst chart of government structure."""
    portfolios = sorted(df["Portfolio"].dropna().unique())
    selected_portfolio = st.selectbox(
        "Select Portfolio (or All)",
        ["All Portfolios"] + list(portfolios),
        key="sunburst_portfolio",
    )

    if selected_portfolio != "All Portfolios":
        filtered = df[df["Portfolio"] == selected_portfolio]
    else:
        filtered = df

    if filtered.empty:
        st.warning("No organisations found.")
        return

    plot_df = filtered.copy()
    plot_df["Count"] = 1

    # Build path depending on whether we're showing all or one portfolio
    if selected_portfolio == "All Portfolios":
        path = ["Portfolio", "Classification", "Type of Body", "Title"]
        max_depth = 2
    else:
        path = ["Portfolio", "Classification", "Type of Body", "Title"]
        max_depth = 4

    fig = px.sunburst(
        plot_df,
        path=path,
        values="Count",
        color="Classification",
        color_discrete_map=CLASSIFICATION_COLORS,
        maxdepth=max_depth,
    )
    fig.update_traces(
        insidetextorientation="radial",
        hovertemplate="<b>%{label}</b><br>Organisations: %{value}<extra></extra>",
    )
    fig.update_layout(
        margin=dict(t=10, l=0, r=0, b=10),
        height=700,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Click on a segment to zoom in. Click the centre to zoom back out.")
