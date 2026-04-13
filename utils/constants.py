"""Central configuration: URLs, color palettes, and classification mappings."""

# CKAN datastore API — returns JSON, supports pagination
CKAN_API_URL = (
    "https://data.gov.au/data/api/3/action/datastore_search"
)
CKAN_RESOURCE_ID = "257663f6-9996-4089-9244-7b205413898f"

# Direct CSV download as fallback
CSV_URL = (
    "https://data.gov.au/data/dataset/"
    "c77cface-69aa-4dd0-b99f-b065dc33c8e6/resource/"
    "257663f6-9996-4089-9244-7b205413898f/download/agor-2025-07-07.csv"
)

CLASSIFICATION_ORDER = {
    "Primary Body": 0,
    "Secondary Statutory Structure": 1,
    "Secondary Non-Statutory Structure": 2,
    "Other Governance Relationship": 3,
}

CLASSIFICATION_COLORS = {
    "Primary Body": "#1B4F72",
    "Secondary Statutory Structure": "#2E86C1",
    "Secondary Non-Statutory Structure": "#5DADE2",
    "Other Governance Relationship": "#AED6F1",
}

TYPE_COLORS = {
    "Non-corporate Commonwealth entity (NCE)": "#1B4F72",
    "Corporate Commonwealth Entity": "#21618C",
    "Commonwealth Company": "#2874A6",
    "Statutory Advisory Structure": "#2E86C1",
    "Statutory Office Holder, Offices and Committees": "#3498DB",
    "Non-Statutory Advisory Structure": "#5DADE2",
    "Non-Statutory Function with Separate Branding": "#85C1E9",
    "Ministerial Councils and Related Bodies": "#F39C12",
    "National Law Bodies": "#E74C3C",
    "Inter-Jurisdictional and International Bodies": "#9B59B6",
    "Structures Linked Through Statutory Contracts/Agreements/Delegations": "#1ABC9C",
    "Joint Ventures, Partnerships and Interests in Other Companies": "#2ECC71",
    "Subsidiaries of Corporate Commonwealth Entities and Commonwealth Companies": "#27AE60",
}

# Display columns for the explorer table
EXPLORER_COLUMNS = [
    "Title",
    "Portfolio",
    "Classification",
    "Type of Body",
    "Parent Organisation",
    "Head Office State",
    "ABN",
]

DETAIL_FIELDS = [
    ("Portfolio", "Portfolio"),
    ("Classification", "Classification"),
    ("Type of Body", "Type of Body"),
    ("Parent Organisation", "Parent Organisation"),
    ("ABN", "ABN"),
    ("Established By / Under", "Established By"),
    ("Head Office State", "State"),
    ("Head Office Suburb", "Suburb"),
    ("Website Address", "Website"),
    ("GFS Sector Classification", "GFS Sector"),
    ("Auditor", "Auditor"),
]
