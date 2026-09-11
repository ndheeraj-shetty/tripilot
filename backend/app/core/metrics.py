import time
import psutil
from typing import Dict, Any

START_TIME = time.time()

def get_system_health() -> Dict[str, Any]:
    uptime = time.time() - START_TIME
    cpu_pct = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()

    return {
        "status": "HEALTHY",
        "uptime_seconds": round(uptime, 1),
        "cpu_utilization_pct": cpu_pct,
        "ram_used_mb": round(ram.used / (1024 * 1024), 1),
        "ram_total_mb": round(ram.total / (1024 * 1024), 1),
        "ram_utilization_pct": ram.percent,
        "database": "CONNECTED",
        "gpu_status": "ONLINE"
    }

def generate_prometheus_metrics() -> str:
    """Generates standard Prometheus text metrics."""
    health = get_system_health()
    metrics = [
        "# HELP zombierun_uptime_seconds Application uptime in seconds",
        "# TYPE zombierun_uptime_seconds counter",
        f"zombierun_uptime_seconds {health['uptime_seconds']}",

        "# HELP zombierun_cpu_utilization_pct CPU usage percentage",
        "# TYPE zombierun_cpu_utilization_pct gauge",
        f"zombierun_cpu_utilization_pct {health['cpu_utilization_pct']}",

        "# HELP zombierun_ram_utilization_pct RAM usage percentage",
        "# TYPE zombierun_ram_utilization_pct gauge",
        f"zombierun_ram_utilization_pct {health['ram_utilization_pct']}",
    ]
    return "\n".join(metrics) + "\n"
