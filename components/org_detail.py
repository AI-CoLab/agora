"""Single organisation detail card."""

import pandas as pd
import streamlit as st

from utils.constants import DETAIL_FIELDS
from utils.hierarchy import get_org_children, get_org_ancestors


def render_org_detail(df: pd.DataFrame):
    """Render a detail card for a selected organisation."""
    org_titles = sorted(df["Title"].dropna().unique())
    selected = st.selectbox(
        "Search and select an organisation",
        org_titles,
        key="org_lookup",
    )

    if not selected:
        return

    matches = df[df["Title"] == selected]
    if matches.empty:
        st.warning("Organisation not found.")
        return

    org = matches.iloc[0]

    # --- Header ---
    st.markdown(f"## {org['Title']}")

    # --- Detail fields in two columns ---
    col1, col2 = st.columns(2)

    fields_left = DETAIL_FIELDS[: len(DETAIL_FIELDS) // 2]
    fields_right = DETAIL_FIELDS[len(DETAIL_FIELDS) // 2 :]

    with col1:
        for col_name, label in fields_left:
            value = org.get(col_name)
            if pd.notna(value) and str(value) != "None":
                if col_name == "Website Address":
                    st.markdown(f"**{label}:** [{value}]({value})")
                else:
                    st.markdown(f"**{label}:** {value}")

    with col2:
        for col_name, label in fields_right:
            value = org.get(col_name)
            if pd.notna(value) and str(value) != "None":
                if col_name == "Website Address":
                    st.markdown(f"**{label}:** [{value}]({value})")
                else:
                    st.markdown(f"**{label}:** {value}")

    # --- Description ---
    if "Description" in org.index:
        desc = org.get("Description")
        if pd.notna(desc) and str(desc) != "None":
            st.divider()
            st.markdown("**Description:**")
            st.markdown(str(desc))

    # --- Established by ---
    established = org.get("Established By / Under")
    extra = org.get("Established by/Under More Info")
    if pd.notna(established) and str(established) != "None":
        st.divider()
        st.markdown("**Enabling Legislation:**")
        st.markdown(str(established))
        if pd.notna(extra) and str(extra) != "None":
            st.markdown(str(extra))

    # --- Ancestry chain ---
    ancestors = get_org_ancestors(df, selected)
    if ancestors:
        st.divider()
        st.markdown("**Organisational Chain:**")
        chain = " → ".join(reversed(ancestors)) + f" → **{selected}**"
        st.markdown(chain)

    # --- Child organisations ---
    children = get_org_children(df, selected)
    if not children.empty:
        st.divider()
        st.markdown(f"**Sub-bodies ({len(children)}):**")
        display_cols = ["Title", "Classification", "Type of Body"]
        display_cols = [c for c in display_cols if c in children.columns]
        st.dataframe(
            children[display_cols],
            use_container_width=True,
            hide_index=True,
        )
