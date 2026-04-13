"""Tree-building helpers for organisational hierarchy."""

import pandas as pd


def get_portfolio_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Return per-portfolio summary counts."""
    stats = (
        df.groupby("Portfolio")
        .agg(
            total=("Title", "count"),
            primary=("Classification", lambda x: (x == "Primary Body").sum()),
            secondary_statutory=(
                "Classification",
                lambda x: (x == "Secondary Statutory Structure").sum(),
            ),
            secondary_non_statutory=(
                "Classification",
                lambda x: (x == "Secondary Non-Statutory Structure").sum(),
            ),
            other=(
                "Classification",
                lambda x: (x == "Other Governance Relationship").sum(),
            ),
            types=("Type of Body", "nunique"),
        )
        .sort_values("total", ascending=False)
        .reset_index()
    )
    return stats


def get_org_children(df: pd.DataFrame, org_title: str) -> pd.DataFrame:
    """Return all organisations that list org_title as their Parent Organisation."""
    if "Parent Organisation" not in df.columns:
        return pd.DataFrame()
    return df[df["Parent Organisation"] == org_title].copy()


def get_org_ancestors(df: pd.DataFrame, org_title: str, max_depth: int = 10) -> list[str]:
    """Walk up the Parent Organisation chain. Returns list from immediate parent to root."""
    ancestors = []
    current = org_title
    seen = set()

    for _ in range(max_depth):
        matches = df[df["Title"] == current]
        if matches.empty:
            break
        parent = matches.iloc[0].get("Parent Organisation", "None")
        if pd.isna(parent) or parent == "None" or parent in seen:
            break
        ancestors.append(parent)
        seen.add(parent)
        current = parent

    return ancestors
