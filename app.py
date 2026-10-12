from __future__ import annotations

from datetime import datetime
import html
import random
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="InfraIntel | WIOCC Concept Demo",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Independent concept demo. All records below are synthetic example data.
# No WIOCC system, data source, or API is connected.
# -----------------------------------------------------------------------------

APP_NAME = "INFRAINTEL"
PAGES = [
    "Executive Command Centre",
    "WIOCC Profile & Strategy",
    "Africa Connectivity Map",
    "Infrastructure & Cable Systems",
    "Network Intelligence",
    "Data Centre Intelligence",
    "Energy & Sustainability",
    "OATS Technical Services",
    "NOC Operations",
    "SLA Monitor",
    "Customer Intelligence",
    "AI Analytics",
    "Reports Centre",
    "Administration",
]

REGIONS = ["Southern Africa", "East Africa", "West Africa", "Central Africa", "Pan-African"]


# Publicly stated company facts are kept separate from synthetic operational records.
# Source pages are linked in the WIOCC Profile & Strategy screen.
PUBLIC_PROFILE = [
    {"Metric": "Digital infrastructure investment", "Value": "≈ US$950 million", "Context": "Publicly reported asset investment"},
    {"Metric": "Subsea systems", "Value": "> 200,000 km", "Context": "Group-reported subsea systems footprint"},
    {"Metric": "Subsea capacity", "Value": "> 150 Tbps", "Context": "Group-reported subsea capacity"},
    {"Metric": "Terrestrial fibre", "Value": "> 115,000 km", "Context": "Group-reported terrestrial fibre footprint"},
    {"Metric": "Data centres", "Value": "> 40", "Context": "Company website headline figure; confirm detailed facility breakdown during discovery"},
    {"Metric": "OADC capacity built", "Value": "25 MW", "Context": "Group-reported capacity built across OADC facilities"},
    {"Metric": "Locations connected", "Value": "1,000+ in 30 countries", "Context": "WIOCC connectivity footprint statement"},
    {"Metric": "Staff footprint", "Value": "> 450 across 15 countries", "Context": "Group-reported workforce footprint"},
]

CABLE_SYSTEMS = [
    {"System": "Equiano", "Type": "Subsea cable", "Publicly documented relationship": "WIOCC identifies fibre-pair ownership on this system", "Potential intelligence use": "International capacity, route diversity and service dependency", "Verification note": "Exact topology, live status and commercial rights require authorised discovery"},
    {"System": "2Africa", "Type": "Subsea cable", "Publicly documented relationship": "WIOCC identifies fibre-pair ownership on this system", "Potential intelligence use": "Capacity, route diversity, landing-station and service dependency", "Verification note": "Exact topology, live status and commercial rights require authorised discovery"},
    {"System": "EASSy", "Type": "Subsea cable", "Publicly documented relationship": "Listed by WIOCC among systems in its connectivity ecosystem", "Potential intelligence use": "International connectivity and resilience view", "Verification note": "Do not infer ownership or route-specific rights from this demo"},
    {"System": "WACS", "Type": "Subsea cable", "Publicly documented relationship": "Listed by WIOCC among systems in its connectivity ecosystem", "Potential intelligence use": "International connectivity and resilience view", "Verification note": "Do not infer ownership or route-specific rights from this demo"},
    {"System": "ACE", "Type": "Subsea cable", "Publicly documented relationship": "WIOCC reports capacity across this and other systems", "Potential intelligence use": "Capacity dependency and service-impact analysis", "Verification note": "Capacity rights and landing details require authorised discovery"},
    {"System": "SEACOM", "Type": "Subsea cable", "Publicly documented relationship": "Listed on WIOCC's regional presence material", "Potential intelligence use": "Connectivity ecosystem context", "Verification note": "This is not a statement of ownership or live service use"},
    {"System": "SAFE", "Type": "Subsea cable", "Publicly documented relationship": "Listed on WIOCC's regional presence material", "Potential intelligence use": "Connectivity ecosystem context", "Verification note": "This is not a statement of ownership or live service use"},
    {"System": "SAT-3", "Type": "Subsea cable", "Publicly documented relationship": "Listed on WIOCC's regional presence material", "Potential intelligence use": "Connectivity ecosystem context", "Verification note": "This is not a statement of ownership or live service use"},
    {"System": "Open-access terrestrial fibre", "Type": "Terrestrial fibre", "Publicly documented relationship": "WIOCC reports a terrestrial and cross-border fibre footprint", "Potential intelligence use": "Route utilisation, fault correlation, protection paths and capacity planning", "Verification note": "Actual route inventory and geospatial data are not included"},
    {"System": "Metro fibre networks", "Type": "Metro network", "Publicly documented relationship": "WIOCC describes metro and long-distance fibre capability in selected markets", "Potential intelligence use": "Metro service visibility, last-mile dependencies and service assurance", "Verification note": "City-level labels in this demo are contextual, not an asset inventory"},
]

OATS_SERVICES = [
    {"Service": "Managed Network Operations Centre (NOC)", "Category": "Operations", "Description": "Managed monitoring and network operations support.", "Example workflow": "Alarm intake → triage → ticket → escalation → closure"},
    {"Service": "Dark fibre management", "Category": "Fibre", "Description": "Managed dark-fibre operations and support.", "Example workflow": "Service request → route check → field task → completion evidence"},
    {"Service": "Managed spectrum", "Category": "Capacity", "Description": "Managed spectrum-related infrastructure operations.", "Example workflow": "Request → allocation review → change approval → update record"},
    {"Service": "Managed capacity termination", "Category": "Capacity", "Description": "Support for capacity termination at appropriate facilities and infrastructure points.", "Example workflow": "Order → location confirmation → work order → verification"},
    {"Service": "Subsea capacity termination", "Category": "Subsea", "Description": "Managed technical support for subsea capacity termination and related infrastructure.", "Example workflow": "Request → landing-station coordination → task tracking → handover"},
    {"Service": "Field services and engineering", "Category": "Field services", "Description": "Installation, troubleshooting, maintenance, compliance and audit support.", "Example workflow": "Dispatch → engineer assignment → visit → evidence → sign-off"},
    {"Service": "Remote hands", "Category": "Data centre", "Description": "On-site technical assistance for equipment and cross-connect tasks.", "Example workflow": "Remote request → access check → task execution → evidence"},
    {"Service": "Equipment logistics", "Category": "Logistics", "Description": "Logistics coordination to support infrastructure deployment across markets.", "Example workflow": "Request → shipment milestone → customs/receipt → inventory handover"},
]

REGIONAL_NODES = [
    {"Location": "Lagos", "Country": "Nigeria", "Region": "West Africa", "Latitude": 6.5244, "Longitude": 3.3792, "Context": "Publicly referenced market / connectivity context"},
    {"Location": "Accra", "Country": "Ghana", "Region": "West Africa", "Latitude": 5.6037, "Longitude": -0.1870, "Context": "Regional connectivity context"},
    {"Location": "Kinshasa", "Country": "DR Congo", "Region": "Central Africa", "Latitude": -4.4419, "Longitude": 15.2663, "Context": "OADC-TEXAF location publicly referenced by WIOCC"},
    {"Location": "Nairobi", "Country": "Kenya", "Region": "East Africa", "Latitude": -1.2921, "Longitude": 36.8219, "Context": "Regional connectivity context"},
    {"Location": "Mombasa", "Country": "Kenya", "Region": "East Africa", "Latitude": -4.0435, "Longitude": 39.6682, "Context": "Regional connectivity context"},
    {"Location": "Johannesburg", "Country": "South Africa", "Region": "Southern Africa", "Latitude": -26.2041, "Longitude": 28.0473, "Context": "OADC / connectivity market context"},
    {"Location": "Durban", "Country": "South Africa", "Region": "Southern Africa", "Latitude": -29.8587, "Longitude": 31.0218, "Context": "OADC / subsea landing market context"},
    {"Location": "Cape Town", "Country": "South Africa", "Region": "Southern Africa", "Latitude": -33.9249, "Longitude": 18.4241, "Context": "OADC / connectivity market context"},
]

# These numbers are intentionally synthetic and are NOT WIOCC ESG or facility measurements.
SUSTAINABILITY_SEED = [
    {"Demo facility": "Sample Core Facility A", "IT load (MW)": 1.80, "Facility power (MW)": 2.72, "PUE": 1.51, "Renewable electricity (%)": 24, "Water intensity (L/kWh)": 1.45, "Emissions (tCO2e / month)": 420},
    {"Demo facility": "Sample Core Facility B", "IT load (MW)": 2.10, "Facility power (MW)": 3.57, "PUE": 1.70, "Renewable electricity (%)": 18, "Water intensity (L/kWh)": 1.62, "Emissions (tCO2e / month)": 565},
    {"Demo facility": "Sample Edge Facility C", "IT load (MW)": 0.48, "Facility power (MW)": 0.70, "PUE": 1.46, "Renewable electricity (%)": 31, "Water intensity (L/kWh)": 1.18, "Emissions (tCO2e / month)": 104},
    {"Demo facility": "Sample Edge Facility D", "IT load (MW)": 0.36, "Facility power (MW)": 0.59, "PUE": 1.64, "Renewable electricity (%)": 12, "Water intensity (L/kWh)": 1.83, "Emissions (tCO2e / month)": 96},
]

NETWORK_SEED = [
    {"Service ID": "SVC-1001", "Service": "Metro Fibre Ring A", "Region": "Southern Africa", "Availability (%)": 99.72, "Utilisation (%)": 74, "Latency (ms)": 18, "Status": "Healthy", "Risk": "Low"},
    {"Service ID": "SVC-1002", "Service": "Cross-Border Backbone B", "Region": "Southern Africa", "Availability (%)": 98.91, "Utilisation (%)": 86, "Latency (ms)": 29, "Status": "Warning", "Risk": "Medium"},
    {"Service ID": "SVC-1003", "Service": "International Capacity C", "Region": "West Africa", "Availability (%)": 96.82, "Utilisation (%)": 91, "Latency (ms)": 54, "Status": "Critical", "Risk": "High"},
    {"Service ID": "SVC-1004", "Service": "Carrier Service D", "Region": "East Africa", "Availability (%)": 99.41, "Utilisation (%)": 67, "Latency (ms)": 24, "Status": "Healthy", "Risk": "Low"},
    {"Service ID": "SVC-1005", "Service": "Regional Fibre Route E", "Region": "Central Africa", "Availability (%)": 98.34, "Utilisation (%)": 82, "Latency (ms)": 38, "Status": "Warning", "Risk": "Medium"},
    {"Service ID": "SVC-1006", "Service": "Cloud Connectivity F", "Region": "Pan-African", "Availability (%)": 99.86, "Utilisation (%)": 59, "Latency (ms)": 21, "Status": "Healthy", "Risk": "Low"},
    {"Service ID": "SVC-1007", "Service": "Backhaul Service G", "Region": "East Africa", "Availability (%)": 97.91, "Utilisation (%)": 88, "Latency (ms)": 42, "Status": "Warning", "Risk": "High"},
    {"Service ID": "SVC-1008", "Service": "Core Transport H", "Region": "West Africa", "Availability (%)": 99.13, "Utilisation (%)": 71, "Latency (ms)": 27, "Status": "Healthy", "Risk": "Low"},
]

FACILITY_SEED = [
    {"Facility": "Johannesburg Core", "Region": "Southern Africa", "Type": "Core", "Utilisation (%)": 73, "Capacity (units)": 100, "Status": "Healthy", "Growth (%)": 8.4},
    {"Facility": "Cape Town Edge", "Region": "Southern Africa", "Type": "Edge", "Utilisation (%)": 66, "Capacity (units)": 70, "Status": "Healthy", "Growth (%)": 6.2},
    {"Facility": "Durban Edge", "Region": "Southern Africa", "Type": "Edge", "Utilisation (%)": 82, "Capacity (units)": 60, "Status": "Warning", "Growth (%)": 10.1},
    {"Facility": "Lagos Core", "Region": "West Africa", "Type": "Core", "Utilisation (%)": 87, "Capacity (units)": 100, "Status": "Warning", "Growth (%)": 12.8},
    {"Facility": "Nairobi Edge", "Region": "East Africa", "Type": "Edge", "Utilisation (%)": 69, "Capacity (units)": 65, "Status": "Healthy", "Growth (%)": 7.3},
    {"Facility": "Kinshasa Core", "Region": "Central Africa", "Type": "Core", "Utilisation (%)": 91, "Capacity (units)": 80, "Status": "Critical", "Growth (%)": 14.6},
    {"Facility": "Accra Edge", "Region": "West Africa", "Type": "Edge", "Utilisation (%)": 61, "Capacity (units)": 55, "Status": "Healthy", "Growth (%)": 5.7},
    {"Facility": "Mombasa Edge", "Region": "East Africa", "Type": "Edge", "Utilisation (%)": 76, "Capacity (units)": 50, "Status": "Healthy", "Growth (%)": 9.2},
]

INCIDENT_SEED = [
    {"Incident ID": "INC-1042", "Title": "Service performance degradation", "Region": "Southern Africa", "Priority": "High", "Status": "Investigating", "Assigned Team": "Network Operations", "Age": "2h 14m", "Service ID": "SVC-1002"},
    {"Incident ID": "INC-1041", "Title": "Capacity threshold exceeded", "Region": "West Africa", "Priority": "Critical", "Status": "Open", "Assigned Team": "Unassigned", "Age": "46m", "Service ID": "SVC-1003"},
    {"Incident ID": "INC-1040", "Title": "Latency above target", "Region": "East Africa", "Priority": "Medium", "Status": "Open", "Assigned Team": "Network Operations", "Age": "1h 08m", "Service ID": "SVC-1007"},
    {"Incident ID": "INC-1039", "Title": "Repeat transport alarm pattern", "Region": "Central Africa", "Priority": "High", "Status": "Escalated", "Assigned Team": "Infrastructure Team", "Age": "3h 26m", "Service ID": "SVC-1005"},
    {"Incident ID": "INC-1038", "Title": "Service availability alert", "Region": "West Africa", "Priority": "Low", "Status": "Investigating", "Assigned Team": "Service Desk", "Age": "34m", "Service ID": "SVC-1008"},
    {"Incident ID": "INC-1037", "Title": "Facility utilisation warning", "Region": "Central Africa", "Priority": "High", "Status": "Open", "Assigned Team": "Data Centre Operations", "Age": "58m", "Service ID": "SVC-1005"},
    {"Incident ID": "INC-1036", "Title": "Interface errors observed", "Region": "Southern Africa", "Priority": "Medium", "Status": "Resolved", "Assigned Team": "Network Operations", "Age": "5h 03m", "Service ID": "SVC-1001"},
    {"Incident ID": "INC-1035", "Title": "Customer service alarm", "Region": "East Africa", "Priority": "Medium", "Status": "Resolved", "Assigned Team": "Service Desk", "Age": "6h 41m", "Service ID": "SVC-1004"},
    {"Incident ID": "INC-1034", "Title": "Power telemetry warning", "Region": "West Africa", "Priority": "High", "Status": "Investigating", "Assigned Team": "Data Centre Operations", "Age": "1h 52m", "Service ID": "SVC-1003"},
    {"Incident ID": "INC-1033", "Title": "Packet loss above threshold", "Region": "Pan-African", "Priority": "Low", "Status": "Resolved", "Assigned Team": "Network Operations", "Age": "Yesterday", "Service ID": "SVC-1006"},
]

SLA_SEED = [
    {"Service ID": "SVC-1001", "Service": "Metro Fibre Ring A", "Region": "Southern Africa", "Target (%)": 99.5, "Actual (%)": 99.72, "Risk": "Low"},
    {"Service ID": "SVC-1002", "Service": "Cross-Border Backbone B", "Region": "Southern Africa", "Target (%)": 99.5, "Actual (%)": 98.91, "Risk": "Medium"},
    {"Service ID": "SVC-1003", "Service": "International Capacity C", "Region": "West Africa", "Target (%)": 99.5, "Actual (%)": 96.82, "Risk": "High"},
    {"Service ID": "SVC-1004", "Service": "Carrier Service D", "Region": "East Africa", "Target (%)": 99.0, "Actual (%)": 99.41, "Risk": "Low"},
    {"Service ID": "SVC-1005", "Service": "Regional Fibre Route E", "Region": "Central Africa", "Target (%)": 99.0, "Actual (%)": 98.34, "Risk": "Medium"},
    {"Service ID": "SVC-1006", "Service": "Cloud Connectivity F", "Region": "Pan-African", "Target (%)": 99.5, "Actual (%)": 99.86, "Risk": "Low"},
    {"Service ID": "SVC-1007", "Service": "Backhaul Service G", "Region": "East Africa", "Target (%)": 99.0, "Actual (%)": 97.91, "Risk": "High"},
    {"Service ID": "SVC-1008", "Service": "Core Transport H", "Region": "West Africa", "Target (%)": 99.0, "Actual (%)": 99.13, "Risk": "Low"},
]

CUSTOMER_SEED = [
    {"Customer ID": "CUS-2001", "Customer": "Atlas Network Services", "Segment": "Carrier", "Services": 18, "SLA (%)": 99.7, "Incidents (30d)": 1, "Status": "Healthy"},
    {"Customer ID": "CUS-2002", "Customer": "BlueBridge Telecom", "Segment": "ISP", "Services": 11, "SLA (%)": 98.4, "Incidents (30d)": 4, "Status": "Review"},
    {"Customer ID": "CUS-2003", "Customer": "Cloudline Africa", "Segment": "Cloud / CDN", "Services": 23, "SLA (%)": 99.8, "Incidents (30d)": 0, "Status": "Healthy"},
    {"Customer ID": "CUS-2004", "Customer": "Continental Carrier Co.", "Segment": "Carrier", "Services": 14, "SLA (%)": 96.9, "Incidents (30d)": 6, "Status": "At risk"},
    {"Customer ID": "CUS-2005", "Customer": "Delta Digital Exchange", "Segment": "Data / Cloud", "Services": 8, "SLA (%)": 99.3, "Incidents (30d)": 2, "Status": "Healthy"},
    {"Customer ID": "CUS-2006", "Customer": "Eastgate Broadband", "Segment": "ISP", "Services": 9, "SLA (%)": 97.4, "Incidents (30d)": 5, "Status": "At risk"},
    {"Customer ID": "CUS-2007", "Customer": "Frontier Mobile Group", "Segment": "Mobile", "Services": 16, "SLA (%)": 99.2, "Incidents (30d)": 2, "Status": "Healthy"},
    {"Customer ID": "CUS-2008", "Customer": "Global Content Routes", "Segment": "Cloud / CDN", "Services": 21, "SLA (%)": 98.8, "Incidents (30d)": 3, "Status": "Review"},
    {"Customer ID": "CUS-2009", "Customer": "Horizon Fibre Partners", "Segment": "Carrier", "Services": 12, "SLA (%)": 99.6, "Incidents (30d)": 1, "Status": "Healthy"},
    {"Customer ID": "CUS-2010", "Customer": "Interswitch Network", "Segment": "ISP", "Services": 7, "SLA (%)": 97.1, "Incidents (30d)": 4, "Status": "At risk"},
]

# State is per Streamlit session; records are examples only.
if "incidents" not in st.session_state:
    st.session_state.incidents = pd.DataFrame(INCIDENT_SEED)
if "oats_requests" not in st.session_state:
    st.session_state.oats_requests = pd.DataFrame(columns=["Request ID", "Service", "Location", "Priority", "Status", "Submitted", "Details"])
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = datetime.now().strftime("%d %b %Y · %H:%M:%S")
if "show_banner" not in st.session_state:
    st.session_state.show_banner = True
if "notifications_enabled" not in st.session_state:
    st.session_state.notifications_enabled = True
if "confirm_resolve" not in st.session_state:
    st.session_state.confirm_resolve = True
if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None
if "last_report" not in st.session_state:
    st.session_state.last_report = None
if "report_generated_at" not in st.session_state:
    st.session_state.report_generated_at = None

# Copies prevent accidental mutation of the source constants.
network_df = pd.DataFrame(NETWORK_SEED)
facilities_df = pd.DataFrame(FACILITY_SEED)
sla_df = pd.DataFrame(SLA_SEED)
customers_df = pd.DataFrame(CUSTOMER_SEED)

# -----------------------------------------------------------------------------
# Styling
# -----------------------------------------------------------------------------

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
      :root { --bg:#08131d; --panel:#101f2c; --panel2:#142635; --line:#253948; --muted:#93a7b8; --text:#edf4f8; --cyan:#40c8d8; --purple:#9b88ff; --orange:#ffb15d; --red:#ff697c; --green:#54d6a0; }
      html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
      .stApp { background: radial-gradient(circle at 80% -10%, #153346 0%, #08131d 42%); color:var(--text); }
      [data-testid="stHeader"] { background:rgba(8,19,29,.80); }
      [data-testid="stSidebar"] { background:#0b1823; border-right:1px solid #203442; }
      [data-testid="stSidebar"] > div:first-child { padding-top:1.1rem; }
      [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#a7bac8; }
      h1,h2,h3 { font-family:'Manrope',sans-serif !important; color:#edf4f8 !important; letter-spacing:-.025em; }
      h1 { font-size:2rem !important; font-weight:800 !important; margin-bottom:.2rem !important; }
      h2 { font-size:1.12rem !important; font-weight:750 !important; }
      h3 { font-size:.98rem !important; font-weight:700 !important; }
      p,li,label,span { color:inherit; }
      .brand-lockup {display:flex;align-items:center;gap:11px;margin:0 0 20px 2px;}
      .brand-mark {display:flex;align-items:flex-end;gap:3px;height:27px;width:30px;}
      .brand-mark i {display:block;width:7px;border-radius:3px 3px 1px 1px;background:var(--cyan);}
      .brand-mark i:nth-child(1){height:14px;opacity:.7}.brand-mark i:nth-child(2){height:22px}.brand-mark i:nth-child(3){height:18px;background:var(--purple);}
      .brand-title {font:800 20px Manrope,sans-serif;letter-spacing:.12em;color:#f1f7fa;}
      .brand-title span {color:var(--cyan);}
      .brand-subtitle {font:600 9px 'DM Sans',sans-serif;letter-spacing:.17em;color:#8ca1b2;margin-top:2px;}
      .demo-tag {display:inline-flex;align-items:center;gap:7px;background:#192a38;border:1px solid #2b4558;color:#b7cad8;border-radius:5px;padding:5px 9px;font-size:10px;font-weight:800;letter-spacing:.13em;}
      .dot {width:7px;height:7px;border-radius:50%;display:inline-block;background:var(--orange);box-shadow:0 0 0 4px #ffb15d16;}
      .hero-sub {color:#9aafbf;font-size:13px;margin-top:0;}
      .section-eyebrow {color:var(--cyan);font-size:10px;font-weight:800;letter-spacing:.17em;text-transform:uppercase;margin-bottom:6px;}
      .sample-warning {background:linear-gradient(90deg,#1a2e3c,#142633);border:1px solid #324b5d;border-left:3px solid var(--orange);padding:12px 15px;border-radius:9px;margin:13px 0 22px;font-size:12px;color:#b9c9d5;}
      .sample-warning strong {color:#f0f6f9;display:block;margin-bottom:3px;font-size:12px;}
      .panel {background:linear-gradient(145deg,rgba(20,38,53,.97),rgba(13,29,41,.97));border:1px solid #263d4d;border-radius:13px;padding:17px 18px;margin-bottom:16px;box-shadow:0 14px 35px rgba(0,0,0,.08);}
      .panel-caption {font-size:11px;color:#91a7b7;margin-top:-5px;margin-bottom:12px;}
      .metric-card {background:linear-gradient(145deg,#142938,#10202d);border:1px solid #2a4354;border-radius:13px;padding:15px 16px 14px;height:127px;}
      .metric-label {display:flex;justify-content:space-between;align-items:center;color:#a4b8c6;font-size:11px;font-weight:600;margin-bottom:9px;}
      .metric-value {font:800 28px Manrope,sans-serif;letter-spacing:-.04em;color:#f1f7fa;line-height:1.1;}
      .metric-foot {font-size:10px;color:#8fa5b5;margin-top:10px;}
      .metric-accent {font-size:10px;font-weight:800;color:var(--green);margin-right:6px;}
      .pill {display:inline-block;padding:4px 8px;border-radius:5px;font-size:10px;font-weight:800;letter-spacing:.04em;border:1px solid transparent;white-space:nowrap;}
      .pill-green {background:#12382f;color:#6ce0b2;border-color:#245e4e;}.pill-yellow {background:#3c3020;color:#ffc77d;border-color:#6e532e;}.pill-red {background:#3a202b;color:#ff8b9b;border-color:#66313f;}.pill-blue {background:#182e42;color:#80c7ff;border-color:#2d4d69;}.pill-purple {background:#2a2545;color:#b3a5ff;border-color:#484074;}
      .small-muted {color:#8fa5b5;font-size:11px;}
      .insight {background:#112634;border:1px solid #294353;border-radius:9px;padding:12px;margin:8px 0;}
      .insight strong {display:block;color:#dceaf1;font-size:12px;margin-bottom:5px;}
      .insight p {font-size:11px;color:#9fb3c1;margin:0;line-height:1.5;}
      .step-chip {display:inline-block;margin:3px 4px 3px 0;padding:7px 10px;border-radius:6px;background:#142c3b;border:1px solid #2e4b5b;font-size:10px;color:#d2e2eb;font-weight:700;}
      .notice {font-size:11px;color:#93a7b8;line-height:1.5;}
      .stButton > button, .stDownloadButton > button {border-radius:8px;border:1px solid #365365;background:#152a39;color:#e6f0f6;font-size:12px;font-weight:700;min-height:2.35rem;transition:all .15s ease;}
      .stButton > button:hover, .stDownloadButton > button:hover {border-color:var(--cyan);color:#fff;background:#1a3545;}
      .stButton > button[kind="primary"] {background:linear-gradient(100deg,#28acbf,#3789b7);border:0;color:#07151c;font-weight:800;}
      .stButton > button[kind="primary"]:hover {filter:brightness(1.08);}
      .stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"] > div,.stNumberInput input {background:#0e1c28 !important;color:#ecf4f8 !important;border-color:#2c4454 !important;border-radius:8px !important;}
      [data-testid="stDataFrame"] {border:1px solid #263d4d;border-radius:9px;overflow:hidden;}
      [data-testid="stMetric"] {background:#132837;border:1px solid #2a4354;padding:13px 15px;border-radius:10px;}
      [data-testid="stMetricLabel"] {color:#9db2c1 !important;font-size:11px !important;}
      [data-testid="stMetricValue"] {color:#f0f6f9 !important;font-family:Manrope,sans-serif;}
      div[data-testid="stTabs"] button {color:#9fb3c1;}
      div[data-testid="stTabs"] button[aria-selected="true"] {color:var(--cyan);}
      .footer {border-top:1px solid #203746;margin-top:24px;padding:14px 0 3px;display:flex;justify-content:space-between;gap:12px;font-size:10px;letter-spacing:.02em;color:#7890a1;}
      .sidebar-note {background:#112430;border:1px solid #243d4e;border-radius:10px;padding:11px;margin-top:18px;font-size:11px;color:#9cb0bf;}
      .sidebar-note strong {color:#e1edf3;display:block;margin-bottom:4px;}
      hr {border-color:#223847 !important;}
      @media(max-width:900px){.metric-card{margin-bottom:7px}.footer{display:block;line-height:1.8}}
    </style>
    """,
    unsafe_allow_html=True,
)


def pill(text: str, tone: str = "blue") -> str:
    tone_map = {"green": "pill-green", "yellow": "pill-yellow", "red": "pill-red", "blue": "pill-blue", "purple": "pill-purple"}
    return f'<span class="pill {tone_map.get(tone, "pill-blue")}">{text}</span>'


def tone_for_status(status: str) -> str:
    s = str(status).lower()
    if any(x in s for x in ["critical", "high", "at risk", "escalated"]):
        return "red"
    if any(x in s for x in ["warning", "medium", "review", "investigating", "open"]):
        return "yellow"
    if any(x in s for x in ["healthy", "normal", "resolved", "low"]):
        return "green"
    return "blue"


def panel_header(title: str, caption: str | None = None) -> None:
    st.markdown(f'<div class="panel"><h3 style="margin:0 0 8px 0">{title}</h3><div class="panel-caption">{caption or ""}</div>', unsafe_allow_html=True)


def panel_end() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def render_table(df: pd.DataFrame, height: int = 330) -> None:
    st.dataframe(df, use_container_width=True, hide_index=True, height=height)


def active_incidents() -> pd.DataFrame:
    df = st.session_state.incidents.copy()
    return df[df["Status"] != "Resolved"]


def count_critical() -> int:
    df = active_incidents()
    return int(df["Priority"].isin(["Critical", "High"]).sum())


def status_card(label: str, value: str, footer: str, icon: str, accent: str = "cyan") -> None:
    accent_color = {"cyan": "#40c8d8", "purple": "#9b88ff", "orange": "#ffb15d", "red": "#ff697c", "green": "#54d6a0"}.get(accent, "#40c8d8")
    st.markdown(
        f'''<div class="metric-card"><div class="metric-label"><span>{label}</span><span style="color:{accent_color};font-size:16px">{icon}</span></div>
        <div class="metric-value">{value}</div><div class="metric-foot">{footer}</div></div>''',
        unsafe_allow_html=True,
    )


def apply_chart_theme(fig: go.Figure, height: int = 300) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "DM Sans, sans-serif", "color": "#a9bdca", "size": 11},
        margin={"l": 8, "r": 8, "t": 22, "b": 8},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#273d4c")
    fig.update_yaxes(gridcolor="#223847", zeroline=False)
    return fig


def generate_ai_answer(question: str) -> tuple[str, list[str]]:
    q = question.lower()
    inc = active_incidents()
    high_inc = inc[inc["Priority"].isin(["Critical", "High"])]
    risky_facilities = facilities_df[facilities_df["Utilisation (%)"] >= 80].sort_values("Utilisation (%)", ascending=False)
    risky_services = network_df[network_df["Risk"].isin(["High", "Medium"])].sort_values("Utilisation (%)", ascending=False)
    if any(word in q for word in ["region", "risk", "highest"]):
        regions = risky_services.groupby("Region").agg(Services=("Service ID", "count"), MaxUtilisation=("Utilisation (%)", "max")).sort_values("MaxUtilisation", ascending=False)
        leaders = ", ".join([f"{r} ({int(row['MaxUtilisation'])}% peak demo utilisation)" for r, row in regions.head(3).iterrows()]) or "No flagged regions found in the demo data."
        return (f"The sample dataset shows the strongest operational risk signals in {leaders}. This is a rule-based summary of illustrative records, not a live network assessment.", ["Review the services contributing to each flagged region.", "Check incidents and SLA records for the same service IDs.", "Validate any risk signal against approved operational telemetry before acting."])
    if any(word in q for word in ["capacity", "utilisation", "utilization", "forecast", "growth"]):
        top = risky_facilities.head(3)
        leaders = ", ".join([f"{row['Facility']} ({row['Utilisation (%)']}% utilisation; {row['Growth (%)']}% illustrative growth)" for _, row in top.iterrows()])
        return (f"The highest facility-utilisation signals in the sample are: {leaders}. The growth values are fictional demonstration figures; capacity forecasts should be recalculated using approved historical data and a validated forecasting method.", ["Review facilities above 80% utilisation.", "Compare planned capacity additions with demand forecasts.", "Confirm data quality, measurement units and reporting periods."])
    if any(word in q for word in ["incident", "critical", "open", "ticket", "alert"]):
        summary = f"There are {len(inc)} unresolved example incidents, including {len(high_inc)} marked High or Critical."
        titles = "; ".join([f"{r['Incident ID']} — {r['Title']} ({r['Priority']}, {r['Status']})" for _, r in high_inc.head(4).iterrows()])
        return (summary + (f" Highest-priority records: {titles}." if titles else " No high-priority incidents remain in the current sample state."), ["Check unassigned critical incidents first.", "Confirm ownership and escalation rules.", "Record investigation notes and resolution evidence in the incident system."])
    if any(word in q for word in ["executive", "summary", "management", "report"]):
        avg_network = network_df["Availability (%)"].mean()
        avg_sla = sla_df["Actual (%)"].mean()
        return (f"Demo executive summary: mean service availability is {avg_network:.2f}% across {len(network_df)} sample network records; mean recorded SLA performance is {avg_sla:.2f}% across {len(sla_df)} sample SLA records; {len(inc)} incidents remain unresolved. These values are illustrative and should not be presented as WIOCC operational metrics.", ["Prioritise high-risk services and facilities.", "Review repeat incidents and SLA shortfalls together.", "Replace all sample records with approved data during a scoped pilot."])
    if any(word in q for word in ["oats", "remote hands", "dark fibre", "dark fiber", "spectrum", "field service", "technical service"]):
        service_names = ", ".join(pd.DataFrame(OATS_SERVICES)["Service"].head(6).tolist())
        return (f"The public OATS service catalogue summary in this demo covers areas such as {service_names}. The screen can demonstrate request intake, assignment, status updates and export, but those actions remain local to this session and do not create real OATS jobs.", ["Confirm the actual service catalogue and ownership with WIOCC/OATS.", "Select one narrow workflow for a controlled pilot.", "Define approvals, evidence, SLA timers and integration points with authorised teams."])
    if any(word in q for word in ["cable", "subsea", "terrestrial", "fibre", "fiber", "connectivity", "eass y", "2africa", "equiano"]):
        systems = ", ".join(pd.DataFrame(CABLE_SYSTEMS)["System"].head(8).tolist())
        return (f"The curated public catalogue references systems and asset categories including {systems}. It separates publicly reported relationships from proposed intelligence use cases. Exact route geometry, service dependencies, capacity rights and live status are intentionally not represented.", ["Validate asset relationships against approved network inventory.", "Add service-to-asset mapping only after formal authorisation.", "Use redundancy and impact calculations only with verified topology and engineering rules."])
    if any(word in q for word in ["sustainability", "energy", "emissions", "renewable", "water", "pue", "esg"]):
        return ("The sustainability screen is a proposed data model for IT load, facility power, PUE, renewable electricity, water intensity and emissions. The values shown are fictional examples; WIOCC's public site links an ESG Report 2025, but no facility ESG measurements are connected here.", ["Agree reporting boundaries, units, scope and measurement periods.", "Ingest approved facility meters and energy invoices.", "Validate calculations with authorised facility and ESG owners before using results externally."])
    if any(word in q for word in ["customer", "client", "commercial"]):
        flagged = customers_df[customers_df["Status"].isin(["At risk", "Review"])].sort_values("SLA (%)")
        names = ", ".join(flagged["Customer"].head(4).tolist())
        return (f"The sample customer table contains {len(flagged)} accounts marked At risk or Review: {names}. These labels are fictional examples and are not assessments of real WIOCC customers.", ["Validate service performance and incident history for flagged accounts.", "Check contractual context before generating account recommendations.", "Restrict customer-level analysis to authorised roles and approved data."])
    return ("I can summarise the built-in demo records for network risk, capacity, incidents, SLA performance, customers, public connectivity catalogue, OATS workflows, sustainability fields or the executive overview. This assistant uses transparent example rules and is not connected to an external AI service.", ["Ask: Which regions have the highest operational risk?", "Ask: Which publicly documented connectivity systems should be reviewed?", "Ask: What data is required for an OADC sustainability dashboard?"])


def make_report_data(report_type: str) -> pd.DataFrame:
    if report_type == "Network performance":
        return network_df.copy()
    if report_type == "SLA report":
        return sla_df.copy()
    if report_type == "Incident register":
        return st.session_state.incidents.copy()
    if report_type == "Infrastructure capacity":
        return facilities_df.copy()
    if report_type == "Customer service overview":
        return customers_df.copy()
    if report_type == "Subsea and terrestrial systems":
        return pd.DataFrame(CABLE_SYSTEMS)
    if report_type == "OATS service catalogue":
        return pd.DataFrame(OATS_SERVICES)
    if report_type == "Africa connectivity nodes":
        return pd.DataFrame(REGIONAL_NODES).drop(columns=["Latitude", "Longitude"])
    if report_type == "Energy and sustainability demo":
        return pd.DataFrame(SUSTAINABILITY_SEED)
    if report_type == "Public WIOCC profile":
        return pd.DataFrame(PUBLIC_PROFILE)
    if report_type == "OATS demo requests":
        return st.session_state.oats_requests.copy()
    return pd.DataFrame(
        [
            {"Metric": "Mean network availability", "Value": f"{network_df['Availability (%)'].mean():.2f}%"},
            {"Metric": "Mean SLA performance", "Value": f"{sla_df['Actual (%)'].mean():.2f}%"},
            {"Metric": "Unresolved sample incidents", "Value": str(len(active_incidents()))},
            {"Metric": "High / critical incidents", "Value": str(count_critical())},
            {"Metric": "Facilities at or above 80% demo utilisation", "Value": str(int((facilities_df['Utilisation (%)'] >= 80).sum()))},
            {"Metric": "Data label", "Value": "Synthetic demo data; not WIOCC operational data"},
        ]
    )


# -----------------------------------------------------------------------------
# Sidebar and top-level shell
# -----------------------------------------------------------------------------

def navigate_to(target_page: str) -> None:
    """Set the sidebar navigation selection before the next script rerun."""
    st.session_state.page_nav = target_page


with st.sidebar:
    st.markdown(
        f'''<div class="brand-lockup"><div class="brand-mark"><i></i><i></i><i></i></div><div><div class="brand-title">INFRA<span>INTEL</span></div><div class="brand-subtitle">DIGITAL INFRASTRUCTURE</div></div></div>
        <div style="margin-bottom:18px"><span class="demo-tag"><span class="dot"></span> DEMO WORKSPACE</span></div>''',
        unsafe_allow_html=True,
    )
    page = st.radio("NAVIGATION", PAGES, label_visibility="collapsed", key="page_nav", format_func=lambda item: {
        "Executive Command Centre": "◈  Executive command centre",
        "WIOCC Profile & Strategy": "◎  WIOCC profile & strategy",
        "Africa Connectivity Map": "⌖  Africa connectivity map",
        "Infrastructure & Cable Systems": "≋  Infrastructure & cable systems",
        "Network Intelligence": "⌁  Network intelligence",
        "Data Centre Intelligence": "▦  Data centre intelligence / OADC",
        "Energy & Sustainability": "♻  Energy & sustainability",
        "OATS Technical Services": "⚒  OATS technical services",
        "NOC Operations": "◉  NOC operations",
        "SLA Monitor": "◷  SLA monitor",
        "Customer Intelligence": "♧  Customer intelligence",
        "AI Analytics": "✳  AI analytics",
        "Reports Centre": "▤  Reports centre",
        "Administration": "⚙  Administration",
    }.get(item, item))
    st.markdown(
        '''<div class="sidebar-note"><strong>Independent concept demo</strong>Uses fictional sample records only. No live WIOCC systems, customer information or operational data are connected.</div>''',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    with st.expander("Demo session controls"):
        if st.button("Refresh sample data", use_container_width=True):
            st.session_state.last_refresh = datetime.now().strftime("%d %b %Y · %H:%M:%S")
            st.toast("Demo view refreshed. Sample values remain illustrative.")
        if st.button("Reset incident workflow", use_container_width=True):
            st.session_state.incidents = pd.DataFrame(INCIDENT_SEED)
            st.toast("Sample incidents reset.")

# Header
now_date = datetime.now().strftime("%A, %d %B %Y").upper()
st.markdown(
    f'''<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:20px;margin:0 0 5px">
      <div><div class="section-eyebrow">WIOCC CONCEPT · {now_date}</div><h1>{page}</h1><div class="hero-sub">Digital infrastructure intelligence, operational analytics and workflow automation.</div></div>
      <div style="text-align:right;min-width:150px"><span class="demo-tag"><span class="dot"></span> SAMPLE DATA</span><div class="small-muted" style="margin-top:8px">Updated {st.session_state.last_refresh}</div></div>
    </div>''',
    unsafe_allow_html=True,
)
if st.session_state.show_banner:
    st.markdown(
        '''<div class="sample-warning"><strong>Concept demonstration · Sample data only</strong>This independent proposal demo is not an official WIOCC product and is not connected to WIOCC systems. All records, names and metrics are illustrative; validate the concept with approved data before any operational use.</div>''',
        unsafe_allow_html=True,
    )
    b1, b2 = st.columns([0.88, 0.12])
    with b2:
        if st.button("Dismiss", key="dismiss_banner"):
            st.session_state.show_banner = False
            st.rerun()

# -----------------------------------------------------------------------------
# Page views
# -----------------------------------------------------------------------------

if page == "Executive Command Centre":
    open_df = active_incidents()
    critical_count = count_critical()
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1: status_card("NETWORK HEALTH", "96.4%", "↑ 1.8% vs previous sample period", "⌁", "cyan")
    with c2: status_card("SLA COMPLIANCE", "98.2%", "↑ 0.6% vs previous sample period", "◷", "purple")
    with c3: status_card("OPEN INCIDENTS", str(len(open_df)), f"{len(open_df[open_df['Status'] == 'Escalated'])} currently escalated", "◉", "orange")
    with c4: status_card("HIGH / CRITICAL", str(critical_count), "Review prioritisation and ownership", "!", "red")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    left, right = st.columns([1.55, 1], gap="large")
    with left:
        st.markdown('<div class="panel"><h3>Infrastructure performance</h3><div class="panel-caption">Illustrative weekly service availability trend · not live telemetry</div>', unsafe_allow_html=True)
        periods = st.selectbox("Time window", ["Last 7 days", "Last 30 days", "Last 90 days"], key="exec_period", label_visibility="collapsed")
        n = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}[periods]
        # Synthetic trend is regenerated deterministically for the selected time window.
        rng = random.Random(n)
        dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=n, freq="D")
        values = [round(max(93.4, min(99.4, 96.1 + rng.uniform(-1.3, 1.5) + i * 0.018)), 2) for i in range(n)]
        trend_df = pd.DataFrame({"Date": dates, "Availability (%)": values, "Target (%)": [99.5] * n})
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=trend_df["Date"], y=trend_df["Availability (%)"], name="Availability", mode="lines", line={"color": "#40c8d8", "width": 3}, fill="tozeroy", fillcolor="rgba(64,200,216,.08)"))
        fig.add_trace(go.Scatter(x=trend_df["Date"], y=trend_df["Target (%)"], name="Illustrative target", mode="lines", line={"color": "#9b88ff", "width": 2, "dash": "dash"}))
        fig.update_yaxes(range=[92, 100], ticksuffix="%")
        st.plotly_chart(apply_chart_theme(fig, 310), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><h3>Regional overview</h3><div class="panel-caption">Example risk signals grouped by region</div>', unsafe_allow_html=True)
        region_df = network_df.groupby("Region", as_index=False).agg(Services=("Service ID", "count"), Availability=("Availability (%)", "mean"), Utilisation=("Utilisation (%)", "mean"))
        region_df["Risk signal"] = region_df["Utilisation"].apply(lambda v: "High" if v >= 85 else "Medium" if v >= 78 else "Low")
        for _, row in region_df.sort_values("Utilisation", ascending=False).iterrows():
            tone = tone_for_status(row["Risk signal"])
            st.markdown(f'''<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;padding:9px 0;border-bottom:1px solid #263d4d"><div><strong style="font-size:12px;color:#e8f1f5">{row['Region']}</strong><div class="small-muted">{row['Services']} services · {row['Availability']:.2f}% avg availability</div></div><div style="text-align:right"><div style="font-size:12px;font-weight:700">{row['Utilisation']:.0f}%</div>{pill(row['Risk signal'].upper(), tone)}</div></div>''', unsafe_allow_html=True)
        st.button("Open Network Intelligence →", type="primary", key="exec_to_network", on_click=navigate_to, args=("Network Intelligence",))
        st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1.2, 1], gap="large")
    with c1:
        st.markdown('<div class="panel"><h3>Priority items</h3><div class="panel-caption">Highest-priority unresolved sample records</div>', unsafe_allow_html=True)
        pri = open_df[open_df["Priority"].isin(["Critical", "High"])].copy()
        if not pri.empty:
            render_table(pri[["Incident ID", "Title", "Region", "Priority", "Status"]].head(5), 240)
        else:
            st.success("No high-priority open sample incidents.")
        st.button("Review incidents →", key="exec_incidents", on_click=navigate_to, args=("NOC Operations",))
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel"><h3>Intelligence signals</h3><div class="panel-caption">Rule-based observations from demo records</div>', unsafe_allow_html=True)
        st.markdown('<div class="insight"><strong>Capacity pressure</strong><p>At least one sample facility is operating above 85% utilisation.</p></div><div class="insight"><strong>SLA exposure</strong><p>Some sample services are below their illustrative availability target.</p></div><div class="insight"><strong>Incident concentration</strong><p>Multiple sample records map to the same regions and service categories.</p></div>', unsafe_allow_html=True)
        st.button("Explore AI Analytics →", key="exec_to_ai", on_click=navigate_to, args=("AI Analytics",))
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "WIOCC Profile & Strategy":
    st.markdown('<div class="section-eyebrow">PUBLIC COMPANY CONTEXT · STRATEGIC ALIGNMENT</div>', unsafe_allow_html=True)
    st.markdown("""
    This page summarises facts published by WIOCC Group and maps them to potential use cases for an independent intelligence and automation pilot. It is not a statement of internal WIOCC priorities or a WIOCC-approved design.
    """)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Terrestrial fibre", ">115,000 km")
    m2.metric("Subsea systems", ">200,000 km")
    m3.metric("Subsea capacity", ">150 Tbps")
    m4.metric("Data centres", ">40")
    st.caption("Publicly reported group figures as shown on WIOCC's website when this demo was prepared (12 October 2026). These are company profile facts, not measurements from the demo.")
    st.markdown("### Strategic context")
    st.markdown('<div class="panel"><h3>Publicly announced investment</h3><div class="panel-caption">Announcement dated 3 September 2026</div><h2 style="font-size:25px!important;color:#40c8d8!important">US$300 million</h2><p>WIOCC stated that the investment from Africa Finance Corporation and Vision Invest is intended to support three priorities: accelerate data-centre capacity deployment and consolidation, extend open-access terrestrial fibre into new markets, and add selected subsea assets that strengthen international connectivity.</p></div>', unsafe_allow_html=True)
    strategic = pd.DataFrame([
        {"Public strategy signal": "Expand and consolidate data-centre capacity", "Potential platform module": "OADC capacity, facility and resilience intelligence", "Pilot question": "Can approved facility data improve visibility of capacity, energy and growth?"},
        {"Public strategy signal": "Extend open-access terrestrial fibre", "Potential platform module": "Fibre inventory, route dependency and capacity intelligence", "Pilot question": "Can route/service inventory and telemetry be consolidated into a consistent view?"},
        {"Public strategy signal": "Add selected subsea assets", "Potential platform module": "Subsea system and service dependency view", "Pilot question": "Can approved service mapping support better impact assessment and reporting?"},
        {"Public strategy signal": "Integrated open-access ecosystem", "Potential platform module": "Cross-domain dashboard and workflow automation", "Pilot question": "Which manual reporting or incident workflows are suitable for an initial pilot?"},
    ])
    st.markdown("### How the concept aligns")
    render_table(strategic, 250)
    st.markdown("### Official public sources")
    s1, s2, s3 = st.columns(3)
    with s1: st.link_button("WIOCC Group overview", "https://wioccgroup.net/", use_container_width=True)
    with s2: st.link_button("US$300m investment announcement", "https://wioccgroup.net/news/wiocc-group-secures-us-300-million-investment", use_container_width=True)
    with s3: st.link_button("Regional presence", "https://wioccgroup.net/regional-presence", use_container_width=True)
    st.info("The concept is an independent proposal. All operational KPIs in other screens remain synthetic sample data; no WIOCC operational systems are connected.")

elif page == "Africa Connectivity Map":
    st.markdown('<div class="section-eyebrow">AFRICAN FOOTPRINT · CONTEXT MAP, NOT ROUTE ENGINEERING</div>', unsafe_allow_html=True)
    st.markdown("The map places a set of publicly referenced African markets and connectivity contexts on a map. Markers are context points only: they do not indicate precise asset locations, live network status or exact fibre/subsea cable routes.")
    nodes_df = pd.DataFrame(REGIONAL_NODES)
    f1, f2 = st.columns([1, 1.5])
    with f1:
        regions_pick = st.multiselect("Show regions", sorted(nodes_df["Region"].unique()), default=sorted(nodes_df["Region"].unique()), key="connectivity_regions")
        table_df = nodes_df[nodes_df["Region"].isin(regions_pick)]
        st.metric("Context locations displayed", len(table_df))
        st.metric("Regions represented", table_df["Region"].nunique())
        st.markdown('<div class="panel"><h3>How to interpret this map</h3><div class="insight"><strong>Public footprint context</strong><p>Locations provide regional context for a proposed cross-domain dashboard; they are not a verified WIOCC asset inventory.</p></div><div class="insight"><strong>Routes intentionally omitted</strong><p>Exact fibre alignments, landing points, cable paths, redundancy and commercial service mappings require approved data.</p></div><div class="insight"><strong>Potential future layer</strong><p>With authorisation, the map could overlay inventory, planned outages, capacity, alerts and service dependencies.</p></div></div>', unsafe_allow_html=True)
    with f2:
        if not table_df.empty:
            fig = px.scatter_geo(table_df, lat="Latitude", lon="Longitude", hover_name="Location", hover_data={"Country": True, "Region": True, "Context": True, "Latitude": False, "Longitude": False}, color="Region", projection="natural earth", title="Illustrative African market/connectivity context")
            fig.update_traces(marker={"size": 11, "line": {"width": 1, "color": "#0b1823"}})
            fig.update_geos(scope="africa", showland=True, landcolor="#162b38", showcountries=True, countrycolor="#365160", showocean=True, oceancolor="#08131d", bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(apply_chart_theme(fig, 540), use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Select at least one region to display the context map.")
    st.markdown("### Location reference table")
    render_table(table_df.drop(columns=["Latitude", "Longitude"]), 280)
    st.link_button("Open WIOCC regional presence page", "https://wioccgroup.net/regional-presence")

elif page == "Infrastructure & Cable Systems":
    st.markdown('<div class="section-eyebrow">SUBSEA · TERRESTRIAL FIBRE · METRO CONNECTIVITY</div>', unsafe_allow_html=True)
    st.markdown("This inventory combines public descriptions of WIOCC's connectivity ecosystem with proposed intelligence use cases. It is not a technical cable-route, capacity-rights or live asset inventory.")
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Subsea systems footprint", ">200,000 km", help="Public WIOCC Group profile figure")
    p2.metric("Subsea capacity", ">150 Tbps", help="Public WIOCC Group profile figure")
    p3.metric("Terrestrial fibre", ">115,000 km", help="Public WIOCC Group profile figure")
    p4.metric("Listed systems/assets", len(CABLE_SYSTEMS), help="Count in this curated demo catalogue, not total WIOCC inventory")
    cable_df = pd.DataFrame(CABLE_SYSTEMS)
    filt1, filt2 = st.columns(2)
    with filt1: type_pick = st.multiselect("Asset type", sorted(cable_df["Type"].unique()), default=sorted(cable_df["Type"].unique()), key="cable_type_filter")
    with filt2: q_cable = st.text_input("Search system or relationship", placeholder="e.g. 2Africa, terrestrial, fibre-pair…", key="cable_search")
    visible = cable_df[cable_df["Type"].isin(type_pick)]
    if q_cable.strip():
        mask = visible.astype(str).apply(lambda col: col.str.contains(q_cable.strip(), case=False, na=False)).any(axis=1)
        visible = visible[mask]
    st.markdown("### Curated public connectivity catalogue")
    render_table(visible, 360)
    if not visible.empty:
        chosen = st.selectbox("Inspect system / asset category", visible["System"].tolist(), key="cable_selected")
        detail = visible[visible["System"] == chosen].iloc[0]
        st.markdown(f"#### {detail['System']}")
        st.write(f"**Publicly documented relationship:** {detail['Publicly documented relationship']}")
        st.write(f"**Potential intelligence use:** {detail['Potential intelligence use']}")
        st.warning(detail["Verification note"])
    st.markdown("### Proposed intelligence layer")
    l1, l2, l3 = st.columns(3)
    with l1: st.markdown('<div class="panel"><h3>Dependency mapping</h3><p>Map services to routes, systems, regions, landing stations and facilities once approved inventory is available.</p></div>', unsafe_allow_html=True)
    with l2: st.markdown('<div class="panel"><h3>Capacity & resilience</h3><p>Compare approved utilisation, protection paths, maintenance windows and contingency capacity.</p></div>', unsafe_allow_html=True)
    with l3: st.markdown('<div class="panel"><h3>Impact assessment</h3><p>Link a validated asset event to potentially affected services and customers, subject to verified mapping.</p></div>', unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1: st.link_button("WIOCC Group overview", "https://wioccgroup.net/")
    with s2: st.link_button("WIOCC regional presence and systems", "https://wioccgroup.net/regional-presence")

elif page == "Energy & Sustainability":
    st.markdown('<div class="section-eyebrow">OADC FACILITY EFFICIENCY · ENERGY · WATER · EMISSIONS</div>', unsafe_allow_html=True)
    st.warning("All facility-level measurements on this page are synthetic examples created for the demo. They are not WIOCC/OADC ESG values or verified performance data.")
    energy_df = pd.DataFrame(SUSTAINABILITY_SEED)
    energy_df["Calculated PUE"] = (energy_df["Facility power (MW)"] / energy_df["IT load (MW)"]).round(2)
    a, b, c, d = st.columns(4)
    a.metric("Average demo PUE", f"{energy_df['Calculated PUE'].mean():.2f}")
    b.metric("Renewable electricity (demo avg)", f"{energy_df['Renewable electricity (%)'].mean():.1f}%")
    c.metric("Demo IT load", f"{energy_df['IT load (MW)'].sum():.2f} MW")
    d.metric("Demo facility power", f"{energy_df['Facility power (MW)'].sum():.2f} MW")
    left, right = st.columns([1.2, 1], gap="large")
    with left:
        st.markdown('<div class="panel"><h3>Energy-efficiency comparison</h3><div class="panel-caption">Illustrative PUE values calculated from synthetic power readings</div>', unsafe_allow_html=True)
        f1 = px.bar(energy_df, x="Demo facility", y="Calculated PUE", color="Calculated PUE", color_continuous_scale=["#40c8d8", "#ffb15d", "#ff697c"])
        f1.update_yaxes(range=[1.0, max(2.0, float(energy_df["Calculated PUE"].max()) + .1)])
        f1.update_xaxes(tickangle=-25)
        st.plotly_chart(apply_chart_theme(f1, 330), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><h3>Potential sustainability data model</h3><div class="panel-caption">Fields to validate with authorised facility owners</div>', unsafe_allow_html=True)
        for title, body in [("Energy", "IT load, total facility power, PUE, peak demand and energy costs."), ("Renewables", "Grid mix, renewable procurement, on-site generation and certificates."), ("Water", "Water consumption, cooling method, reuse and water intensity."), ("Emissions", "Scope boundaries, grid factors, generator fuel and reporting period."), ("Resilience", "Backup power tests, cooling alarms, maintenance and site-level risks.")]:
            st.markdown(f'<div class="insight"><strong>{title}</strong><p>{body}</p></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("### Illustrative facility efficiency register")
    render_table(energy_df, 280)
    st.markdown("### Public context")
    st.write("WIOCC's website includes an ESG and Sustainability section with an ESG Report 2025. The concept dashboard should use approved, validated site data and the applicable reporting definitions before drawing any conclusions.")
    st.link_button("WIOCC ESG & Sustainability", "https://wioccgroup.net/esg-and-sustainability")

elif page == "OATS Technical Services":
    st.markdown('<div class="section-eyebrow">OPEN ACCESS TECHNICAL SERVICES · WORKFLOW CONCEPT</div>', unsafe_allow_html=True)
    st.markdown("This screen models how a digital workflow layer could support intake, dispatch and reporting around technical service activities. It does not create a live OATS order or notify a WIOCC team.")
    oats_df = pd.DataFrame(OATS_SERVICES)
    r1, r2, r3 = st.columns(3)
    r1.metric("Service categories in catalogue", len(oats_df))
    r2.metric("Demo requests in session", len(st.session_state.oats_requests))
    r3.metric("Open demo requests", int((st.session_state.oats_requests["Status"] != "Resolved").sum()) if not st.session_state.oats_requests.empty else 0)
    category_filter = st.multiselect("Filter service categories", sorted(oats_df["Category"].unique()), default=sorted(oats_df["Category"].unique()), key="oats_category_filter")
    show_oats = oats_df[oats_df["Category"].isin(category_filter)]
    st.markdown("### Service catalogue")
    render_table(show_oats, 300)
    st.markdown("### Create a demo service request")
    with st.form("oats_request_form", clear_on_submit=True):
        service_choice = st.selectbox("Service", oats_df["Service"].tolist())
        location_choice = st.selectbox("Location / market", ["South Africa", "Nigeria", "DR Congo", "Kenya", "Ghana", "Other / to be confirmed"])
        priority_choice = st.selectbox("Priority", ["Normal", "High", "Critical"])
        details_choice = st.text_area("Request details", placeholder="Describe the demo requirement; do not include confidential information.")
        submitted = st.form_submit_button("Create demo request", type="primary")
    if submitted:
        next_num = 1 if st.session_state.oats_requests.empty else len(st.session_state.oats_requests) + 1
        new_row = pd.DataFrame([{"Request ID": f"OATS-DEMO-{next_num:04d}", "Service": service_choice, "Location": location_choice, "Priority": priority_choice, "Status": "Open", "Submitted": datetime.now().strftime("%d %b %Y %H:%M"), "Details": details_choice.strip() or "No additional details provided"}])
        st.session_state.oats_requests = pd.concat([st.session_state.oats_requests, new_row], ignore_index=True)
        st.success(f"Created {new_row.iloc[0]['Request ID']} in this demo session only.")
    if not st.session_state.oats_requests.empty:
        st.markdown("### Demo request register")
        requests_df = st.session_state.oats_requests.copy()
        render_table(requests_df, 240)
        chosen_request = st.selectbox("Select request to update", requests_df["Request ID"].tolist(), key="oats_selected_request")
        next_status = st.selectbox("Set status", ["Open", "Assigned", "In progress", "Escalated", "Resolved"], key="oats_next_status")
        if st.button("Update demo request status", key="oats_update_status"):
            st.session_state.oats_requests.loc[st.session_state.oats_requests["Request ID"] == chosen_request, "Status"] = next_status
            st.success(f"{chosen_request} updated to {next_status} in this session.")
            st.rerun()
        st.download_button("Export OATS demo requests (CSV)", st.session_state.oats_requests.to_csv(index=False).encode("utf-8"), file_name="oats_demo_requests.csv", mime="text/csv")
    st.markdown("### Workflow example")
    for step in ["Request intake", "Triage and validate", "Assign team / engineer", "Execute technical task", "Capture evidence", "Confirm handover", "Close and report"]:
        st.markdown(f'<span class="step-chip">{step}</span>', unsafe_allow_html=True)
    st.link_button("WIOCC Open Access Technical Services", "https://wioccgroup.net/open-access-technical-services")

elif page == "Network Intelligence":
    st.markdown('<div class="section-eyebrow">SERVICE HEALTH · UTILISATION · REGIONAL SIGNALS</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Services in sample", len(network_df))
    c2.metric("Mean availability", f"{network_df['Availability (%)'].mean():.2f}%")
    c3.metric("High/medium risk services", int(network_df["Risk"].isin(["High", "Medium"]).sum()))
    left, right = st.columns([1.3, 1], gap="large")
    with left:
        st.markdown('<div class="panel"><h3>Service utilisation by region</h3><div class="panel-caption">Synthetic utilisation figures by example service</div>', unsafe_allow_html=True)
        fig = px.bar(network_df.sort_values("Utilisation (%)", ascending=True), x="Utilisation (%)", y="Service", color="Risk", orientation="h", color_discrete_map={"Low": "#54d6a0", "Medium": "#ffb15d", "High": "#ff697c"})
        fig.update_xaxes(range=[0, 100], ticksuffix="%")
        st.plotly_chart(apply_chart_theme(fig, 360), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><h3>Filters</h3><div class="panel-caption">Explore the sample network inventory</div>', unsafe_allow_html=True)
        region_pick = st.multiselect("Region", sorted(network_df["Region"].unique()), default=list(network_df["Region"].unique()), key="network_region_filter")
        risk_pick = st.multiselect("Risk", ["Low", "Medium", "High"], default=["Low", "Medium", "High"], key="network_risk_filter")
        min_util = st.slider("Minimum utilisation", 0, 100, 0, 5, key="network_min_util")
        st.markdown(f'<div class="notice">Showing services in {len(region_pick)} selected regions with risk {", ".join(risk_pick) or "(none)"}.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    filtered = network_df[network_df["Region"].isin(region_pick) & network_df["Risk"].isin(risk_pick) & (network_df["Utilisation (%)"] >= min_util)]
    st.markdown('<div class="panel"><h3>Network service inventory</h3><div class="panel-caption">Choose a row from the filtered records</div>', unsafe_allow_html=True)
    render_table(filtered, 330)
    if not filtered.empty:
        selected_service = st.selectbox("Inspect service", filtered["Service ID"].tolist(), key="network_service_detail")
        rec = filtered[filtered["Service ID"] == selected_service].iloc[0]
        a, b, c, d = st.columns(4)
        a.metric("Availability", f"{rec['Availability (%)']:.2f}%")
        b.metric("Utilisation", f"{rec['Utilisation (%)']}%")
        c.metric("Latency", f"{rec['Latency (ms)']} ms")
        d.metric("Risk", rec["Risk"])
        st.button("View related incidents →", key="network_related_incidents", on_click=navigate_to, args=("NOC Operations",))
    else:
        st.info("No sample records match these filters.")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Data Centre Intelligence":
    st.markdown('<div class="section-eyebrow">OADC CONTEXT · FACILITY CAPACITY · UTILISATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><h3>Publicly reported OADC context</h3><div class="panel-caption">Company profile facts; not measurements from the sample facility table</div>', unsafe_allow_html=True)
    pub1, pub2, pub3 = st.columns(3)
    pub1.metric("Data-centre footprint", ">40 facilities")
    pub2.metric("OADC capacity built", "25 MW")
    pub3.metric("Published footprint markets", "South Africa · Nigeria · DRC")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("The table and graphs below use synthetic example facility records, not a verified OADC facility inventory.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Facilities in demo", len(facilities_df))
    c2.metric("Mean demo utilisation", f"{facilities_df['Utilisation (%)'].mean():.1f}%")
    c3.metric("Demo facilities above 80%", int((facilities_df["Utilisation (%)"] >= 80).sum()))
    c4.metric("Highest illustrative growth", f"{facilities_df['Growth (%)'].max():.1f}%")
    left, right = st.columns([1.25, 1], gap="large")
    with left:
        st.markdown('<div class="panel"><h3>Facility utilisation</h3><div class="panel-caption">Thresholds shown for demo analysis only</div>', unsafe_allow_html=True)
        fig = px.bar(facilities_df.sort_values("Utilisation (%)"), x="Utilisation (%)", y="Facility", orientation="h", color="Status", color_discrete_map={"Healthy": "#54d6a0", "Warning": "#ffb15d", "Critical": "#ff697c"})
        fig.add_vline(x=80, line_dash="dash", line_color="#ffb15d", annotation_text="80% review threshold")
        fig.update_xaxes(range=[0, 100], ticksuffix="%")
        st.plotly_chart(apply_chart_theme(fig, 380), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><h3>Demand and risk signals</h3><div class="panel-caption">Illustrative growth rate vs utilisation</div>', unsafe_allow_html=True)
        fig2 = px.scatter(facilities_df, x="Utilisation (%)", y="Growth (%)", text="Facility", size="Capacity (units)", color="Status", color_discrete_map={"Healthy": "#54d6a0", "Warning": "#ffb15d", "Critical": "#ff697c"})
        fig2.update_traces(textposition="top center", marker={"opacity": 0.85})
        fig2.update_xaxes(range=[50, 100], ticksuffix="%")
        fig2.update_yaxes(ticksuffix="%")
        st.plotly_chart(apply_chart_theme(fig2, 380), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><h3>Facility register</h3><div class="panel-caption">Sample facility locations and utilisation values; not a verified inventory</div>', unsafe_allow_html=True)
    render_table(facilities_df.sort_values("Utilisation (%)", ascending=False), 320)
    st.markdown('<div class="notice">Capacity decisions require validated telemetry, unit definitions, redundancy rules, approved forecasts and engineering review.</div></div>', unsafe_allow_html=True)

elif page == "NOC Operations":
    inc = st.session_state.incidents.copy()
    open_inc = active_incidents()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Unresolved", len(open_inc))
    c2.metric("Critical / high", count_critical())
    c3.metric("Escalated", int((inc["Status"] == "Escalated").sum()))
    c4.metric("Resolved", int((inc["Status"] == "Resolved").sum()))
    st.markdown("### Incident workbench")
    f1, f2, f3 = st.columns([1, 1, 1.2])
    with f1: status_filter = st.multiselect("Status", sorted(inc["Status"].unique()), default=sorted(inc["Status"].unique()), key="incident_status_filter")
    with f2: priority_filter = st.multiselect("Priority", ["Critical", "High", "Medium", "Low"], default=["Critical", "High", "Medium", "Low"], key="incident_priority_filter")
    with f3: query = st.text_input("Search incidents", placeholder="ID, title, region, team…", key="incident_search")
    filtered = inc[inc["Status"].isin(status_filter) & inc["Priority"].isin(priority_filter)]
    if query.strip():
        mask = filtered.astype(str).apply(lambda col: col.str.contains(query.strip(), case=False, na=False)).any(axis=1)
        filtered = filtered[mask]
    st.markdown('<div class="panel"><h3>Incident register</h3><div class="panel-caption">Changes to incident status and assignment persist during this Streamlit session only</div>', unsafe_allow_html=True)
    render_table(filtered, 300)
    st.markdown("</div>", unsafe_allow_html=True)
    if len(inc):
        st.markdown('<div class="panel"><h3>Incident actions</h3><div class="panel-caption">Choose an example incident and perform a demo workflow action</div>', unsafe_allow_html=True)
        selected_id = st.selectbox("Incident ID", inc["Incident ID"].tolist(), key="incident_action_id")
        selected = inc[inc["Incident ID"] == selected_id].iloc[0]
        st.markdown(f"**{selected['Title']}**  ·  {selected['Region']}  ·  {pill(selected['Priority'].upper(), tone_for_status(selected['Priority']))}  {pill(selected['Status'].upper(), tone_for_status(selected['Status']))}", unsafe_allow_html=True)
        x1, x2, x3, x4 = st.columns(4)
        with x1:
            if st.button("Assign to me", use_container_width=True, key="incident_assign"):
                st.session_state.incidents.loc[st.session_state.incidents["Incident ID"] == selected_id, "Assigned Team"] = "Demo Operations Manager"
                st.toast(f"{selected_id} assigned to Demo Operations Manager.")
                st.rerun()
        with x2:
            if st.button("Mark investigating", use_container_width=True, key="incident_investigate"):
                st.session_state.incidents.loc[st.session_state.incidents["Incident ID"] == selected_id, "Status"] = "Investigating"
                st.toast(f"{selected_id} moved to Investigating.")
                st.rerun()
        with x3:
            if st.button("Escalate", use_container_width=True, key="incident_escalate"):
                st.session_state.incidents.loc[st.session_state.incidents["Incident ID"] == selected_id, "Status"] = "Escalated"
                st.session_state.incidents.loc[st.session_state.incidents["Incident ID"] == selected_id, "Priority"] = "High" if selected["Priority"] not in ["Critical"] else "Critical"
                st.toast(f"{selected_id} escalated in the demo workflow.")
                st.rerun()
        with x4:
            resolve_ok = True
            if st.session_state.confirm_resolve:
                resolve_ok = st.checkbox("Confirm resolution", key=f"confirm_{selected_id}")
            if st.button("Resolve incident", use_container_width=True, disabled=not resolve_ok, key="incident_resolve"):
                st.session_state.incidents.loc[st.session_state.incidents["Incident ID"] == selected_id, "Status"] = "Resolved"
                st.toast(f"{selected_id} marked resolved in the demo.")
                st.rerun()
        note = st.text_area("Investigation note (session only)", placeholder="Add a demo note or handover details…", key=f"note_{selected_id}", height=80)
        if st.button("Save demo note", key="save_incident_note"):
            st.session_state[f"saved_note_{selected_id}"] = note
            st.success(f"Note saved in this session for {selected_id}.")
        if st.session_state.get(f"saved_note_{selected_id}"):
            st.caption(f"Saved note: {st.session_state[f'saved_note_{selected_id}']}")
        st.markdown('<div class="notice">These actions update only in-memory demo records. They do not notify real teams or update any ticketing system.</div></div>', unsafe_allow_html=True)

elif page == "SLA Monitor":
    current = sla_df.copy()
    current["Variance (pp)"] = (current["Actual (%)"] - current["Target (%)"]).round(2)
    misses = current[current["Variance (pp)"] < 0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Mean sample performance", f"{current['Actual (%)'].mean():.2f}%")
    c2.metric("Services below target", len(misses))
    c3.metric("High-risk service records", int((current["Risk"] == "High").sum()))
    left, right = st.columns([1.2, 1], gap="large")
    with left:
        st.markdown('<div class="panel"><h3>SLA actual vs target</h3><div class="panel-caption">Illustrative SLA values; contract rules not validated</div>', unsafe_allow_html=True)
        long_sla = current.melt(id_vars=["Service"], value_vars=["Target (%)", "Actual (%)"], var_name="Measure", value_name="Performance (%)")
        fig = px.bar(long_sla, x="Service", y="Performance (%)", color="Measure", barmode="group", color_discrete_map={"Target (%)": "#9b88ff", "Actual (%)": "#40c8d8"})
        fig.update_yaxes(range=[94, 100], ticksuffix="%")
        fig.update_xaxes(tickangle=-35)
        st.plotly_chart(apply_chart_theme(fig, 340), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><h3>Services requiring review</h3><div class="panel-caption">Sample records with negative variance to target</div>', unsafe_allow_html=True)
        if misses.empty:
            st.success("No shortfalls in current sample records.")
        else:
            for _, row in misses.iterrows():
                st.markdown(f'''<div style="padding:10px 0;border-bottom:1px solid #263d4d"><div style="display:flex;justify-content:space-between;gap:10px"><strong style="font-size:12px">{row['Service']}</strong>{pill(f"{row['Variance (pp)']:.2f} pp", "red")}</div><div class="small-muted">{row['Region']} · Actual {row['Actual (%)']:.2f}% vs target {row['Target (%)']:.2f}%</div></div>''', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><h3>SLA detail register</h3><div class="panel-caption">Filter and inspect example SLA records</div>', unsafe_allow_html=True)
    filter_sla = st.multiselect("Risk category", ["Low", "Medium", "High"], default=["Low", "Medium", "High"], key="sla_risk_filter")
    render_table(current[current["Risk"].isin(filter_sla)].sort_values("Variance (pp)"), 300)
    st.button("Open NOC incidents →", key="sla_to_noc", on_click=navigate_to, args=("NOC Operations",))
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Customer Intelligence":
    customers = customers_df.copy()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Demo accounts", len(customers))
    c2.metric("Services represented", int(customers["Services"].sum()))
    c3.metric("Accounts marked at risk", int((customers["Status"] == "At risk").sum()))
    c4.metric("Mean recorded SLA", f"{customers['SLA (%)'].mean():.2f}%")
    left, right = st.columns([1, 1.1], gap="large")
    with left:
        st.markdown('<div class="panel"><h3>Account status mix</h3><div class="panel-caption">Illustrative statuses across example account records</div>', unsafe_allow_html=True)
        stat = customers.groupby("Status", as_index=False).size()
        fig = px.pie(stat, names="Status", values="size", hole=.64, color="Status", color_discrete_map={"Healthy": "#54d6a0", "Review": "#ffb15d", "At risk": "#ff697c"})
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(apply_chart_theme(fig, 310), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><h3>Service quality by account</h3><div class="panel-caption">Sample SLA value vs incident count</div>', unsafe_allow_html=True)
        fig2 = px.scatter(customers, x="Incidents (30d)", y="SLA (%)", size="Services", hover_name="Customer", color="Status", color_discrete_map={"Healthy": "#54d6a0", "Review": "#ffb15d", "At risk": "#ff697c"})
        fig2.update_yaxes(range=[95, 100], ticksuffix="%")
        st.plotly_chart(apply_chart_theme(fig2, 310), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    search = st.text_input("Search customer or segment", placeholder="Type account name, ID or segment…", key="customer_search")
    customer_filtered = customers
    if search.strip():
        customer_filtered = customers[customers.astype(str).apply(lambda col: col.str.contains(search.strip(), case=False, na=False)).any(axis=1)]
    st.markdown('<div class="panel"><h3>Customer portfolio</h3><div class="panel-caption">All names are fictional placeholders for product demonstration</div>', unsafe_allow_html=True)
    render_table(customer_filtered, 310)
    if not customer_filtered.empty:
        customer_id = st.selectbox("Open account profile", customer_filtered["Customer ID"].tolist(), key="customer_profile_select")
        rec = customer_filtered[customer_filtered["Customer ID"] == customer_id].iloc[0]
        st.markdown(f"#### {rec['Customer']}  {pill(str(rec['Status']).upper(), tone_for_status(rec['Status']))}", unsafe_allow_html=True)
        q1, q2, q3 = st.columns(3)
        q1.metric("Services", int(rec["Services"]))
        q2.metric("SLA", f"{rec['SLA (%)']:.1f}%")
        q3.metric("Incidents / 30 days", int(rec["Incidents (30d)"]))
        st.caption("Profile metrics are demo records only; validate contractual and privacy requirements before production use.")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "AI Analytics":
    st.markdown('<div class="section-eyebrow">RULE-BASED SAMPLE ANALYTICS · NOT CONNECTED TO AN EXTERNAL AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><h3>Ask Infrastructure Intelligence</h3><div class="panel-caption">Ask a question about the built-in network, capacity, SLA, incident or customer examples. Responses are generated by transparent demo rules.</div>', unsafe_allow_html=True)
    prompts = ["Which regions have the highest operational risk?", "Where is capacity utilisation increasing fastest?", "Summarise open critical incidents.", "Which connectivity systems should be reviewed?", "What data belongs in an ESG dashboard?"]
    cols = st.columns(len(prompts))
    for idx, prompt in enumerate(prompts):
        with cols[idx]:
            if st.button(prompt, key=f"ai_prompt_{idx}", use_container_width=True):
                st.session_state.ai_question = prompt
    question = st.text_area("Your question", key="ai_question", placeholder="e.g. Which regions have the highest operational risk?", height=95)
    a1, a2 = st.columns([1, 4])
    with a1:
        run_ai = st.button("Run analysis ✳", type="primary", key="run_ai_analysis", use_container_width=True)
    with a2:
        st.markdown('<div class="notice" style="padding-top:9px">No live network data is accessed. Results are calculated from the example records packaged with this app.</div>', unsafe_allow_html=True)
    if run_ai:
        answer, recommendations = generate_ai_answer(question.strip())
        st.session_state.last_analysis = {"question": question.strip(), "answer": answer, "recommendations": recommendations, "time": datetime.now().strftime("%d %b %Y %H:%M:%S")}
    if st.session_state.last_analysis:
        result = st.session_state.last_analysis
        st.markdown(f'''<div class="insight" style="padding:16px;margin-top:18px"><div class="section-eyebrow">ANALYSIS RESULT · {result['time']}</div><strong style="font-size:14px">{html.escape(result['question'] or 'Analysis')}</strong><p style="font-size:13px;line-height:1.7;margin-top:8px">{result['answer']}</p></div>''', unsafe_allow_html=True)
        st.markdown("#### Recommended next steps")
        for i, action in enumerate(result["recommendations"], 1):
            st.markdown(f'<div class="step-chip">{i}. {action}</div>', unsafe_allow_html=True)
        st.download_button("Download analysis note", data=(f"Question: {result['question']}\n\nAnalysis: {result['answer']}\n\nRecommendations:\n" + "\n".join(f"- {x}" for x in result["recommendations"])).encode("utf-8"), file_name="infraintel_demo_analysis.txt", mime="text/plain")
    else:
        st.info("Choose one of the suggested questions or type your own, then click Run analysis.")
    st.markdown("</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="panel"><h3>Data available to this demo</h3><div class="panel-caption">Small synthetic data snapshots included in app.py</div>', unsafe_allow_html=True)
        for title, subtitle, count in [("Network services", "Availability, utilisation, region and risk", len(network_df)), ("Incident records", "Priority, ownership and workflow status", len(st.session_state.incidents)), ("SLA records", "Targets, actuals and risk labels", len(sla_df)), ("Facilities", "Capacity utilisation and illustrative growth", len(facilities_df)), ("Customer accounts", "Fictional account service-quality records", len(customers_df))]:
            st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #263d4d;padding:10px 0"><div><strong style="font-size:12px">{title}</strong><div class="small-muted">{subtitle}</div></div><b style="color:#40c8d8">{count}</b></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel"><h3>Production considerations</h3><div class="panel-caption">Required before deployment to operational environments</div>', unsafe_allow_html=True)
        for title, body in [("Approved data access", "Document source systems, permissions, ownership and retention."), ("Evaluation and guardrails", "Validate answer quality, false positives, thresholds and escalation outcomes."), ("Security and auditing", "Implement identity, role-based permissions, audit logs and secrets management."), ("Human oversight", "Keep operational decisions and critical workflow approvals with authorised staff.")]:
            st.markdown(f'<div class="insight"><strong>{title}</strong><p>{body}</p></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Reports Centre":
    st.markdown('<div class="section-eyebrow">REPORT BUILDER · EXPORTABLE DEMO OUTPUTS</div>', unsafe_allow_html=True)
    report_types = ["Executive summary", "Network performance", "SLA report", "Incident register", "Infrastructure capacity", "Customer service overview", "Subsea and terrestrial systems", "OATS service catalogue", "Africa connectivity nodes", "Energy and sustainability demo", "Public WIOCC profile", "OATS demo requests"]
    st.markdown('<div class="panel"><h3>Build a report</h3><div class="panel-caption">Generate a downloadable CSV, JSON or text summary from the sample dataset.</div>', unsafe_allow_html=True)
    r1, r2, r3 = st.columns([1.25, 1, 1])
    with r1: report_type = st.selectbox("Report type", report_types, key="report_type")
    with r2: period = st.selectbox("Reporting period", ["Last 7 days", "Last 30 days", "Current month", "Quarter to date"], key="report_period")
    with r3: report_format = st.selectbox("Format", ["CSV", "JSON", "Text summary"], key="report_format")
    if st.button("Generate report ↗", type="primary", key="generate_report"):
        data = make_report_data(report_type)
        st.session_state.last_report = {"type": report_type, "period": period, "format": report_format, "data": data, "generated": datetime.now().strftime("%d %b %Y · %H:%M:%S")}
        st.session_state.report_generated_at = st.session_state.last_report["generated"]
        st.toast(f"{report_type} generated from the demo dataset.")
    if st.session_state.last_report:
        report = st.session_state.last_report
        public_source_reports = {"Subsea and terrestrial systems", "OATS service catalogue", "Africa connectivity nodes", "Public WIOCC profile"}
        report_badge = "PUBLIC SOURCE SUMMARY" if report["type"] in public_source_reports else "DEMO DATA"
        st.markdown(f"#### Preview: {report['type']}  {pill(report_badge, 'blue' if report_badge == 'PUBLIC SOURCE SUMMARY' else 'yellow')}", unsafe_allow_html=True)
        st.caption(f"Period selected: {report['period']} · Generated {report['generated']}")
        render_table(report["data"], 280)
        data = report["data"]
        safe_name = report["type"].lower().replace(" ", "_")
        if report["format"] == "CSV":
            payload = data.to_csv(index=False).encode("utf-8")
            filename, mime = f"{safe_name}_demo.csv", "text/csv"
        elif report["format"] == "JSON":
            payload = data.to_json(orient="records", indent=2).encode("utf-8")
            filename, mime = f"{safe_name}_demo.json", "application/json"
        else:
            content = f"{report['type']}\nReporting period: {report['period']}\nGenerated: {report['generated']}\n\nPROVENANCE NOTE: Independent concept demo. Operational KPI, incident, customer, facility and sustainability records are synthetic. Public company facts/catalogue summaries are paraphrased from linked official WIOCC pages and are not a verified internal asset inventory.\n\n{data.to_string(index=False)}"
            payload = content.encode("utf-8")
            filename, mime = f"{safe_name}_demo.txt", "text/plain"
        st.download_button(f"Download {report['format']}", data=payload, file_name=filename, mime=mime, type="primary", key="download_report")
    else:
        st.info("Select the report options above and click Generate report to view and download the result.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("### Report templates")
    cards = st.columns(3)
    report_descriptions = {
        "Executive summary": "KPIs, risks and priority signals",
        "Network performance": "Availability, utilisation and region",
        "SLA report": "Target vs actual service performance",
        "Incident register": "Priorities, assignment and workflow status",
        "Infrastructure capacity": "Facility utilisation and synthetic growth",
        "Customer service overview": "Fictional account service-quality records",
        "Subsea and terrestrial systems": "Curated public connectivity catalogue",
        "OATS service catalogue": "Publicly described technical-service areas",
        "Africa connectivity nodes": "Context locations; not exact route mapping",
        "Energy and sustainability demo": "Synthetic example energy and facility readings",
        "Public WIOCC profile": "Publicly reported company profile metrics",
        "OATS demo requests": "Requests entered in this demo session",
    }
    for i, title in enumerate(report_types):
        col = cards[i % 3]
        with col:
            st.markdown(f'<div class="panel" style="min-height:110px"><strong style="font-size:13px;color:#e7f1f6">{title}</strong><div class="small-muted" style="margin-top:8px">{report_descriptions[title]}</div></div>', unsafe_allow_html=True)


elif page == "Administration":
    st.markdown('<div class="section-eyebrow">WORKSPACE CONFIGURATION · INTEGRATION PLACEHOLDERS</div>', unsafe_allow_html=True)
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown('<div class="panel"><h3>Demo workspace settings</h3><div class="panel-caption">These controls apply to this running app session only</div>', unsafe_allow_html=True)
        st.session_state.notifications_enabled = st.toggle("Enable local demo notifications", value=st.session_state.notifications_enabled, key="toggle_notifications")
        st.session_state.confirm_resolve = st.toggle("Require confirmation before resolving incidents", value=st.session_state.confirm_resolve, key="toggle_confirm_resolve")
        show = st.toggle("Show sample-data disclaimer", value=st.session_state.show_banner, key="toggle_banner_setting")
        st.session_state.show_banner = show
        if st.button("Save settings", type="primary", key="save_admin_settings"):
            st.toast("Demo settings saved for this session.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div class="panel"><h3>Example access roles</h3><div class="panel-caption">Conceptual roles only; authentication is not implemented</div>', unsafe_allow_html=True)
        for role, desc, count in [("Administrator", "Workspace configuration, users and audit logs", "1 example"), ("Operations manager", "Incident workflows, SLA views and reports", "4 examples"), ("Business analyst", "Analytics, customers and management reports", "7 examples"), ("Executive viewer", "Read-only summary dashboards", "3 examples")]:
            st.markdown(f'<div style="padding:10px 0;border-bottom:1px solid #263d4d;display:flex;justify-content:space-between;gap:12px"><div><strong style="font-size:12px">{role}</strong><div class="small-muted">{desc}</div></div><span class="small-muted">{count}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><h3>Integration readiness</h3><div class="panel-caption">Proposed connection points for a discovery phase</div>', unsafe_allow_html=True)
        integrations = [
            ("Network management systems", "Read-only metrics, alarms and inventory", "NOT CONNECTED"),
            ("Ticketing / ITSM", "Incident create, update and status sync", "NOT CONNECTED"),
            ("Data warehouse / BI", "Approved reporting and analytics data", "NOT CONNECTED"),
            ("Messaging / notifications", "Approved escalation channels", "NOT CONNECTED"),
            ("Identity provider", "Single sign-on and role-based access", "NOT CONNECTED"),
            ("Facility energy / ESG data", "Approved power, cooling, water and emissions measurements", "NOT CONNECTED"),
            ("Asset / GIS inventory", "Approved subsea, terrestrial, metro and site asset mapping", "NOT CONNECTED"),
        ]
        for title, desc, status in integrations:
            st.markdown(f'<div style="padding:12px 0;border-bottom:1px solid #263d4d;display:flex;justify-content:space-between;gap:12px;align-items:center"><div><strong style="font-size:12px">{title}</strong><div class="small-muted">{desc}</div></div>{pill(status, "yellow")}</div>', unsafe_allow_html=True)
        st.markdown('<div class="notice" style="margin-top:13px">Do not add passwords, API keys or production endpoints to this concept demo. A production implementation needs an approved architecture, secret storage, access controls and security assessment.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><h3>Session status</h3><div class="panel-caption">Basic diagnostics for this prototype session</div>', unsafe_allow_html=True)
    st.write({"App": APP_NAME, "Build": "Streamlit Concept Demo V2", "Data sources connected": 0, "Session refresh": st.session_state.last_refresh, "Incident records in session": len(st.session_state.incidents), "Notifications enabled": st.session_state.notifications_enabled})
    if st.button("Reset all demo state", key="reset_all_state"):
        for key in ["incidents", "oats_requests", "last_refresh", "show_banner", "notifications_enabled", "confirm_resolve", "last_analysis", "last_report", "report_generated_at"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    f'''<div class="footer"><span>INFRAINTEL · CONCEPT DEMO V2</span><span>Independent proposal concept · No WIOCC endorsement implied</span><span>Session refreshed: {st.session_state.last_refresh}</span></div>''',
    unsafe_allow_html=True,
)
