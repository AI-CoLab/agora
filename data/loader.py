"""Fetch, cache, and clean the AGOR dataset via CKAN API or CSV download."""

import json
import urllib.request

import pandas as pd
import streamlit as st

from utils.constants import (
    CKAN_API_URL,
    CKAN_RESOURCE_ID,
    CSV_URL,
    CLASSIFICATION_ORDER,
)


@st.cache_data(ttl=3600, show_spinner="Loading Australian Government organisations data...")
def load_agor_data() -> pd.DataFrame:
    """Fetch AGOR data via CKAN datastore API, falling back to CSV download."""
    df = _fetch_via_ckan_api()
    if df is None:
        df = _fetch_via_csv()
    if df is None:
        st.error(
            "Could not load data from data.gov.au. "
            "Please check your internet connection and try again."
        )
        st.stop()
    return clean_dataframe(df)


def _fetch_via_ckan_api() -> pd.DataFrame | None:
    """Fetch all records from the CKAN datastore API with pagination."""
    try:
        records = []
        offset = 0
        limit = 500

        while True:
            url = (
                f"{CKAN_API_URL}"
                f"?resource_id={CKAN_RESOURCE_ID}"
                f"&limit={limit}&offset={offset}"
            )
            req = urllib.request.Request(url, headers={"User-Agent": "AGOR-Explorer/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            if not data.get("success"):
                return None

            result = data["result"]
            batch = result.get("records", [])
            if not batch:
                break

            records.extend(batch)
            offset += limit

            # Stop if we've fetched all records
            total = result.get("total", 0)
            if offset >= total:
                break

        if not records:
            return None

        df = pd.DataFrame(records)
        # Drop CKAN internal columns
        df = df.drop(columns=["_id"], errors="ignore")
        return df

    except Exception:
        return None


def _fetch_via_csv() -> pd.DataFrame | None:
    """Download the CSV file directly."""
    try:
        return pd.read_csv(CSV_URL, encoding="utf-8-sig")
    except Exception:
        return None


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names, fill gaps, and add derived columns."""
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Strip whitespace from all string columns
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": pd.NA, "None": pd.NA, "": pd.NA})

    # Fill missing parent organisations
    if "Parent Organisation" in df.columns:
        df["Parent Organisation"] = df["Parent Organisation"].fillna("None")

    # Add classification sort order
    if "Classification" in df.columns:
        df["Classification Order"] = (
            df["Classification"].map(CLASSIFICATION_ORDER).fillna(99).astype(int)
        )
        df = df.sort_values(
            ["Classification Order", "Portfolio", "Title"]
        ).reset_index(drop=True)

    return df
