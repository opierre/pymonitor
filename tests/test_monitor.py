"""Integration tests for the PyMonitor Python wrapper and Rust backend."""

import json
import threading
import time

import paho.mqtt.client as mqtt_client
import pytest
from pymonitor.monitor import ExporterType, PyMonitor

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "pymonitor/metrics"

# Fields expected in every published JSON payload
REQUIRED_METRIC_KEYS = {
    "cpu_usage",
    "cpu_brand",
    "ram_percent",
    "max_ram",
    "disk_percent",
    "available_disk",
    "boot_time",
    "os_name",
    "os_version",
    "kernel_version",
    "hostname",
    "core_count_logical",
    "swap_total",
    "swap_used",
    "network_rx_bytes",
    "network_tx_bytes",
    "network_interfaces",
    "per_core_usage",
    "load_avg_1m",
    "load_avg_5m",
    "load_avg_15m",
    "users",
    "top_processes",
}


# ---------------------------------------------------------------------------
# Existing metric tests
# ---------------------------------------------------------------------------


def test_get_process_metrics() -> None:
    """Test that the Rust backend returns process metrics."""
    monitor = PyMonitor()
    processes = monitor.get_process_metrics("python")
    assert isinstance(processes, list)
    for process in processes:
        assert isinstance(process, tuple)
        assert len(process) == 3


def test_global_metrics() -> None:
    """Test that the Rust backend successfully returns global metrics."""
    monitor = PyMonitor()
    metrics = monitor.get_global_metrics()
    
    assert isinstance(metrics.cpu_usage, float)
    assert isinstance(metrics.cpu_brand, str)
    assert isinstance(metrics.ram_percent, float)
    assert isinstance(metrics.max_ram, int)
    assert isinstance(metrics.disk_percent, float)
    assert isinstance(metrics.available_disk, int)
    assert isinstance(metrics.boot_time, int)
    assert metrics.ram_percent > 0
    assert metrics.max_ram > 0
    assert metrics.available_disk > 0
    assert metrics.boot_time > 0
