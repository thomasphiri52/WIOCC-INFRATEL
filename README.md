# InfraIntel — WIOCC Digital Infrastructure Intelligence Concept Demo V2

A Streamlit application demonstrating a possible cross-domain intelligence and workflow layer aligned to publicly described WIOCC Group business areas: subsea and terrestrial connectivity, OADC data-centre operations, OATS technical services, regional infrastructure context, network/SLA views, incident workflows, sustainability data modelling, and management reporting.

## What's new in V2

- **WIOCC Profile & Strategy**: public company profile figures and the 3 September 2026 US$300 million investment announcement, with official source links.
- **Africa Connectivity Map**: map of selected African market/context locations. Markers are context-only and do not show exact cable, fibre or asset routes.
- **Infrastructure & Cable Systems**: searchable curated catalogue that distinguishes publicly described relationships from unknown asset details and potential analytics use cases.
- **OADC / Data Centre Intelligence**: public group-level context separated from synthetic demo facility readings.
- **Energy & Sustainability**: example data model and fictional metrics for IT load, facility power, PUE, renewable electricity, water intensity and emissions.
- **OATS Technical Services**: service catalogue, demo request intake, status update workflow and CSV export.
- **Expanded report exports**: report types for public company facts, connectivity catalogue, connectivity context locations, OATS service catalogue and requests, and synthetic sustainability data.
- **AI analytics prompts**: rule-based demo responses for connectivity, OATS workflow and sustainability questions.

## Important disclosure

- This is an independent concept demo, not an official WIOCC product and not affiliated with or endorsed by WIOCC.
- Public company-level facts are paraphrased from the official WIOCC URLs listed below and can change. Confirm figures directly with WIOCC before reusing them in a formal proposal.
- The public connectivity catalogue is not a verified internal WIOCC asset list. It does not provide cable-route geometry, live network status, exact capacity rights, customer-to-asset mapping or engineering topology.
- All incident records, customer accounts, service KPIs, facility utilisation/growth readings, energy/water/emissions values and workflow requests are synthetic examples.
- The map's locations provide regional context and are not an exact inventory of WIOCC assets or cable routes.
- No WIOCC system, network-management platform, ticketing product, customer record, ESG data source, GIS inventory, or live AI service is connected.
- Incident and OATS request actions update the current Streamlit session only. They do not notify real staff or update external systems.
- There is no production authentication. Do not deploy with sensitive data or treat this as an operational monitoring tool.

## Public reference links

- WIOCC Group overview and headline figures: <https://wioccgroup.net/>
- WIOCC Group profile: <https://wioccgroup.net/wiocc>
- WIOCC's US$300 million investment announcement (3 September 2026): <https://wioccgroup.net/news/wiocc-group-secures-us-300-million-investment>
- Regional presence and connectivity context: <https://wioccgroup.net/regional-presence>
- Open Access Technical Services (OATS): <https://wioccgroup.net/open-access-technical-services>
- Open Access Data Centres (OADC): <https://wioccgroup.net/open-access-data-centres>
- ESG and Sustainability: <https://wioccgroup.net/esg-and-sustainability>

## Run locally

1. Install Python 3.10 or later.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL printed by Streamlit, usually `http://localhost:8501`.

On Windows, you can instead double-click `run_app.bat`. It installs dependencies and launches Streamlit.

## Deploy to Streamlit Community Cloud

1. Upload the contents of this folder to a GitHub repository.
2. In Streamlit Community Cloud, create an app from that repository.
3. Set the main file path to `app.py`.
4. Deploy. The platform installs dependencies from `requirements.txt`.

Keep `app.py`, `requirements.txt`, `run_app.bat`, `README.md` and `.streamlit/config.toml` in the repository root (with `.streamlit/config.toml` in its subfolder).

## Included screens

- Executive Command Centre
- WIOCC Profile & Strategy
- Africa Connectivity Map
- Infrastructure & Cable Systems
- Network Intelligence
- Data Centre Intelligence / OADC context
- Energy & Sustainability
- OATS Technical Services
- NOC Operations
- SLA Monitor
- Customer Intelligence
- AI Analytics (transparent rule-based sample logic)
- Reports Centre (CSV, JSON and text exports)
- Administration / Integration Readiness

## Before any production use

A real implementation would need WIOCC discovery and approval, authorised system/data access, verified asset and service inventory, role-based authentication, secure secrets management, integration design, validated metric definitions, alert/forecast testing, audit logging, data-retention controls, a security review, and formal operational ownership.
