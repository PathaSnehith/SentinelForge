# SentinelForge – Campus SOC Simulator

SentinelForge is a major cybersecurity project that simulates a modern Security Operations Center (SOC). It ingests authentication and activity logs, persists them in SQLite, runs real-time detection analytics, and exposes the results via a FastAPI backend plus an offline CLI workflow. Use it to demonstrate blue-team operations, showcase detection logic, or extend it into your own SOC platform.

## Architecture

- **FastAPI backend (`app/main.py`)** – REST endpoints for log ingestion, alert retrieval, health checks, and dashboard hosting.
- **SQLite persistence (`app/database.py`, `app/models.py`)** – durable storage for raw telemetry and generated alerts.
- **Detection engine (`app/detections.py`)** – modular rules for brute-force attacks, impossible travel, and high-volume data exfiltration.
- **Service layer (`app/services.py`)** – shared logic for parsing logs, running detections, and returning consolidated results.
- **Offline analyzer (`analyze_logs.py`)** – command-line tool to batch process datasets without the API.
- **Training datasets (`data/*.json`)** – **13,000+ log entries** across 5 large-scale datasets for comprehensive training:
  - `dataset_1_brute_force.json` (~1,256 entries)
  - `dataset_2_data_theft.json` (~2,117 entries)
  - `dataset_3_privilege_abuse.json` (~2,012 entries)
  - `dataset_4_comprehensive.json` (~2,618 entries)
  - `dataset_5_massive_training.json` (~5,120 entries)
- **Demo dataset (`data/sample_logs.json`)** – 13 entries for quick testing.
- **Web dashboard (`static/*`)** – a zero-dependency frontend that visualizes alerts/logs with dataset selector dropdown.
- **Dataset generator (`generate_large_datasets.py`)** – script to generate additional large training datasets.

## Quick Start

```powershell
cd "C:\Users\patha\Downloads\Key Looger"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Run API + dashboard (http://localhost:8000/)
uvicorn app.main:app --reload

# In another terminal, ingest sample logs through the API
Invoke-RestMethod -Uri http://localhost:8000/demo/ingest-sample -Method Post

# Fetch alerts
Invoke-RestMethod -Uri http://localhost:8000/alerts
```

## Dashboard Tour

1. Browse to `http://localhost:8000/` after starting Uvicorn.
2. **Select a dataset** from the dropdown menu (includes all 5 large training datasets + demo dataset).
3. Click **"Ingest Selected Dataset"** to load and analyze the chosen dataset.
4. The dashboard auto-refreshes every 15s, showing alert counts, details, and recent telemetry.
5. Use browser dev tools or tweak `static/app.js` to extend the UI (filters, charts, etc.).

**Note:** For training purposes, start with `dataset_5_massive_training.json` (5,120 entries) for comprehensive analysis.

## Offline SOC Drill

```bash
# Quick demo (13 entries)
python analyze_logs.py --file data/sample_logs.json

# Large training dataset (5,120 entries)
python analyze_logs.py --file data/dataset_5_massive_training.json

# Other training datasets
python analyze_logs.py --file data/dataset_1_brute_force.json
python analyze_logs.py --file data/dataset_2_data_theft.json
python analyze_logs.py --file data/dataset_3_privilege_abuse.json
python analyze_logs.py --file data/dataset_4_comprehensive.json
```

This command ingests the dataset, writes entries to SQLite, and prints generated alerts:

- `BRUTE_FORCE` – repeated failed logins.
- `IMPOSSIBLE_TRAVEL` – logins from distant geolocations within 1 hour.
- `DATA_EXFIL` – downloads >200 MB on sensitive resources.
- `ADMIN_AFTER_HOURS` – privileged users logging in outside business hours.
- `SENSITIVE_RESOURCE_ANOM` – sensitive downloads from unmanaged devices.
- `UNAUTHORIZED_PRIV_ACTION` – non-admins executing changes such as `config_change`.
- `LOW_SUCCESS_RATE` – anomalously high login failure ratios on a device.

## Extending the Project

- Add new detectors (phishing clicks, privilege escalation) by creating functions in `app/detections.py` and registering them in `DETECTORS`.
- Wire a React or Streamlit dashboard to the `/alerts` endpoint for visual SOC metrics.
- Schedule `analyze_logs.py` via cron/Task Scheduler to process daily log drops.
- Replace SQLite with PostgreSQL or integrate with message queues (Kafka) for streaming workloads.

