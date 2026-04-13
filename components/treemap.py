"""Portfolio treemap visualisation using Plotly."""

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.constants import CLASSIFICATION_COLORS


def render_treemap(df: pd.DataFrame):
    """Render an interactive treemap of government organisations."""
    # Filter controls
    classifications = sorted(df["Classification"].dropna().unique())
    selected = st.multiselect(
        "Filter by Classification",
        options=classifications,
        default=classifications,
        key="treemap_class_filter",
    )

    filtered = df[df["Classification"].isin(selected)] if selected else df

    if filtered.empty:
        st.warning("No organisations match the selected filters.")
        return

    # Build treemap with hierarchical path
    # Add a count column for sizing
    plot_df = filtered.copy()
    plot_df["Count"] = 1

    fig = px.treemap(
        plot_df,
        path=["Classification", "Portfolio", "Type of Body", "Title"],
        values="Count",
        color="Classification",
        color_discrete_map=CLASSIFICATION_COLORS,
        maxdepth=3,
    )
    fig.update_layout(
        margin=dict(t=30, l=0, r=0, b=0),
        height=700,
    )
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Organisations: %{value}<extra></extra>",
        textinfo="label+value",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Click on a section to zoom in. Click the header bar to zoom back out.")
