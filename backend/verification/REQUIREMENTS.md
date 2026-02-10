# Whereisfire.py — Requirements

## Overview

`Whereisfire.py` is a verification script that:

- **Fire detection** — Queries NASA FIRMS (VIIRS) for active fire data in a bounding box and computes a wildfire likelihood metric.
- **Flood data** — Fetches river discharge and flood forecast data from Open-Meteo and Copernicus (CEMS GloFAS).

## Environment

- **Python:** 3.9+
- **OS:** Any (script uses standard paths; bash install script is written for Unix/macOS/Git Bash).

## Python Dependencies

| Package | Purpose |
|--------|---------|
| `python-dotenv` | Loads `.env` (API keys, config) into the environment. |
| `pandas` | DataFrames and time series for FIRMS CSV and flood daily data. |
| `requests` | HTTP calls (also used by other libs). |
| `pyproj` | Geodetic calculations (area/perimeter of bounding box for likelihood). |
| `shapely` | Polygon geometry (currently used for bounding-box representation). |
| `openmeteo-requests` | Client for Open-Meteo APIs (e.g. flood API). |
| `requests-cache` | Caching for Open-Meteo requests. |
| `retry-requests` | Retries with backoff for Open-Meteo. |
| `cdsapi` | Copernicus Climate Data Store API (GloFAS historical). |

See `requirements.txt` in this directory for installable list.

## Environment Variables (.env)

Create a `.env` file in the same directory as `Whereisfire.py`:

| Variable | Description |
|----------|-------------|
| `NASAFIREPRIVATEKEY` | NASA FIRMS / MODAPS map key for fire API access. |
| `FLOOD_KEY` | Copernicus CDS/EWDS API key for GloFAS (optional if hardcoded fallback exists). |

Other vars (e.g. `DOMAIN`, `ADMIN_EMAIL`, `ROOT_URL`) are not used by this script but may be used by other tools sharing the same `.env`.

## External Services

- **NASA FIRMS:** [https://firms.modaps.eosdis.nasa.gov/](https://firms.modaps.eosdis.nasa.gov/) — requires MAP key.
- **Open-Meteo Flood API:** [https://flood-api.open-meteo.com/](https://flood-api.open-meteo.com/) — no key required.
- **Copernicus CDS/EWDS:** [https://ewds.climate.copernicus.eu/](https://ewds.climate.copernicus.eu/) — requires API key for GloFAS.

## Installation

From the `verification` directory:

```bash
./install_requirements.sh
```

Or manually:

```bash
pip install -r requirements.txt
```

## Usage

Run from project root or from `verification`:

```bash
python verification/Whereisfire.py
```

Or from inside `verification`:

```bash
python Whereisfire.py
```

The script loads `.env` from the same directory as the script, so the working directory does not need to be `verification`.
