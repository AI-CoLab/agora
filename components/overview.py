"""Overview dashboard with KPI metrics and summary charts."""

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.constants import CLASSIFICATION_COLORS, TYPE_COLORS


def render_overview(df: pd.DataFrame):
    """Render the overview dashboard with metrics and charts."""
    # --- KPI metrics row ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Organisations", f"{len(df):,}")
    with col2:
        st.metric("Portfolios", df["Portfolio"].nunique())
    with col3:
        primary_count = (df["Classification"] == "Primary Body").sum()
        st.metric("Primary Bodies", f"{primary_count:,}")
    with col4:
        secondary_count = df["Classification"].str.contains("Secondary", na=False).sum()
        st.metric("Secondary Bodies", f"{secondary_count:,}")

    st.divider()

    # --- Organisations per portfolio (horizontal bar) ---
    st.subheader("Organisations by Portfolio")
    portfolio_counts = (
        df.groupby("Portfolio")
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=True)
    )
    fig_bar = px.bar(
        portfolio_counts,
        x="Count",
        y="Portfolio",
        orientation="h",
        color_discrete_sequence=["#002E5D"],
        height=max(400, len(portfolio_counts) * 28),
    )
    fig_bar.update_layout(
        margin=dict(l=0, r=20, t=10, b=10),
        yaxis_title="",
        xaxis_title="Number of Organisations",
        showlegend=False,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # --- Classification and Type of Body donut charts ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("By Classification")
        class_counts = (
            df.groupby("Classification")
            .size()
            .reset_index(name="Count")
            .sort_values("Count", ascending=False)
        )
        fig_class = px.pie(
            class_counts,
            values="Count",
            names="Classification",
            hole=0.45,
            color="Classification",
            color_discrete_map=CLASSIFICATION_COLORS,
        )
        fig_class.update_traces(textposition="outside", textinfo="label+value")
        fig_class.update_layout(
            margin=dict(l=0, r=0, t=10, b=10),
            showlegend=False,
            height=400,
        )
        st.plotly_chart(fig_class, use_container_width=True)

    with col_right:
        st.subheader("By Type of Body")
        type_counts = (
            df.groupby("Type of Body")
            .size()
            .reset_index(name="Count")
            .sort_values("Count", ascending=False)
        )
        fig_type = px.pie(
            type_counts,
            values="Count",
            names="Type of Body",
            hole=0.45,
            color="Type of Body",
            color_discrete_map=TYPE_COLORS,
        )
        fig_type.update_traces(textposition="outside", textinfo="label+value")
        fig_type.update_layout(
            margin=dict(l=0, r=0, t=10, b=10),
            showlegend=False,
            height=400,
        )
        st.plotly_chart(fig_type, use_container_width=True)
