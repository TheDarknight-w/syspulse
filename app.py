from __future__ import annotations

import os
import platform
from datetime import datetime, timezone

import psutil
from flask import Flask, jsonify, render_template

app = Flask(__name__)


def get_processes(limit: int = 8) -> list[dict]:
    rows = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            info = proc.info
            rows.append({
                "pid": info.get("pid"),
                "name": info.get("name") or "unknown",
                "cpu_percent": round(info.get("cpu_percent") or 0.0, 2),
                "memory_percent": round(info.get("memory_percent") or 0.0, 2),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return sorted(rows, key=lambda x: x["cpu_percent"], reverse=True)[:limit]


def collect_metrics() -> dict:
    vm = psutil.virtual_memory()
    disk_path = os.getenv("SYSPULSE_DISK_PATH", "/")
    disk = psutil.disk_usage(disk_path)
    cpu = psutil.cpu_percent(interval=0.2)
    boot_time = datetime.fromtimestamp(psutil.boot_time(), tz=timezone.utc)
    now = datetime.now(timezone.utc)
    return {
        "timestamp": now.isoformat(),
        "hostname": platform.node(),
        "platform": platform.platform(),
        "cpu_percent": round(cpu, 2),
        "memory": {"total_bytes": vm.total, "used_bytes": vm.used,
                   "available_bytes": vm.available, "percent": round(vm.percent, 2)},
        "disk": {"path": disk_path, "total_bytes": disk.total, "used_bytes": disk.used,
                 "free_bytes": disk.free, "percent": round(disk.percent, 2)},
        "uptime_seconds": max(0, int(now.timestamp() - boot_time.timestamp())),
        "processes": get_processes(),
    }


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "SysPulse"})


@app.get("/api/metrics")
def metrics():
    try:
        return jsonify(collect_metrics())
    except (OSError, psutil.Error) as exc:
        app.logger.exception("Unable to collect system metrics")
        return jsonify({"error": "Unable to collect system metrics", "detail": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
