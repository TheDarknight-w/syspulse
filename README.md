# SysPulse — Linux System Health Dashboard

A lightweight Python/Flask dashboard for CPU, memory, disk, uptime and process monitoring, with a Bash CLI snapshot script and Docker support.

## Features
- JSON metrics API at `/api/metrics` and service check at `/api/health`.
- Browser dashboard refreshes every five seconds.
- Top processes sorted by CPU usage.
- Bash snapshot script for terminal-based inspection.
- Dockerfile and Docker Compose configuration.

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000.

## Run with Docker
```bash
docker compose up --build
```
Open http://127.0.0.1:5000. Metrics inside a container reflect the container's visible process and resource environment; they are not guaranteed to represent every host-level metric.

## Bash snapshot (Linux)
```bash
chmod +x scripts/collect_system_info.sh
./scripts/collect_system_info.sh
```

## Tests
```bash
python -m unittest discover -s tests -v
```

## Tech stack
Python, Flask, psutil, Bash, HTML, CSS, JavaScript, Docker.
