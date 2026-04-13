"""Searchable and filterable organisation data table."""

import pandas as pd
import streamlit as st

from utils.constants import EXPLORER_COLUMNS


def render_explorer(df: pd.DataFrame):
    """Render a searchable, filterable organisation explorer."""
    # --- Search ---
    search_term = st.text_input(
        "Search organisations",
        placeholder="e.g. CSIRO, Defence, Arts, Health...",
        key="explorer_search",
    )

    # --- Filters ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        portfolio_opts = sorted(df["Portfolio"].dropna().unique())
        selected_portfolios = st.multiselect("Portfolio", portfolio_opts, key="explorer_portfolio")
    with col2:
        class_opts = sorted(df["Classification"].dropna().unique())
        selected_classes = st.multiselect("Classification", class_opts, key="explorer_class")
    with col3:
        type_opts = sorted(df["Type of Body"].dropna().unique())
        selected_types = st.multiselect("Type of Body", type_opts, key="explorer_type")
    with col4:
        if "Head Office State" in df.columns:
            state_opts = sorted(df["Head Office State"].dropna().unique())
            selected_states = st.multiselect("State", state_opts, key="explorer_state")
        else:
            selected_states = []

    # --- Apply filters ---
    filtered = df.copy()

    if search_term:
        search_lower = search_term.lower()
        mask = filtered.apply(
            lambda row: any(
                search_lower in str(val).lower()
                for val in row[["Title", "Portfolio", "Type of Body"]].values
            ),
            axis=1,
        )
        # Also search Description if present
        if "Description" in filtered.columns:
            mask = mask | filtered["Description"].astype(str).str.lower().str.contains(
                search_lower, na=False
            )
        filtered = filtered[mask]

    if selected_portfolios:
        filtered = filtered[filtered["Portfolio"].isin(selected_portfolios)]
    if selected_classes:
        filtered = filtered[filtered["Classification"].isin(selected_classes)]
    if selected_types:
        filtered = filtered[filtered["Type of Body"].isin(selected_types)]
    if selected_states and "Head Office State" in filtered.columns:
        filtered = filtered[filtered["Head Office State"].isin(selected_states)]

    # --- Results count ---
    st.markdown(f"**{len(filtered):,}** organisations found")

    # --- Display table ---
    display_cols = [c for c in EXPLORER_COLUMNS if c in filtered.columns]
    column_config = {}
    if "Website Address" in filtered.columns:
        display_cols.append("Website Address")
        column_config["Website Address"] = st.column_config.LinkColumn("Website")

    st.dataframe(
        filtered[display_cols],
        use_container_width=True,
        height=600,
        column_config=column_config,
        hide_index=True,
    )

    # --- Download button ---
    csv_data = filtered[display_cols].to_csv(index=False)
    st.download_button(
        "Download filtered data as CSV",
        csv_data,
        "agor_filtered.csv",
        "text/csv",
        key="explorer_download",
    )
