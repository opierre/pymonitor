"""A lightweight monitor for computer constants."""
from enum import Enum

from . import _rust_monitor


class ExporterType(str, Enum):
    """Supported backend exporter types."""

    MQTT = "mqtt"
    VICTORIAMETRICS = "victoriametrics"



class PyMonitor:
    """A lightweight monitor for computer constants.

    This class provides a Python interface to the Rust-based
    system monitoring tools. It should allow for background polling
    and pushing data directly to a database.
    """

    def __init__(self):
        """Initialize PyMonitor instance."""
        self._monitor_handle: _rust_monitor.MonitorHandle | None = None

    def start(self) -> None:
    def start(self, refresh_rate: int = 5, exporter_type: ExporterType = ExporterType.MQTT, priority: int = 5) -> None:
        """Starts the background Rust monitoring thread.

        Args:
            refresh_rate: polling interval in seconds. Defaults to 5.
            exporter_type: type of exporter to use. Defaults to ExporterType.MQTT.
            priority: thread priority from 0 (highest) to 5 (lowest). Defaults to 5.

        Raises:
            RuntimeError: if the monitor is already actively running.
        """
        if self._monitor_handle is not None:
            raise RuntimeError("Monitor is already running.")
        # Start monitoring thread
        self._monitor_handle = _rust_monitor.start_monitoring("", self._interval)

    def stop(self) -> None:
        """Stops the background Rust monitoring thread."""
        if self._monitor_handle is not None:
            self._monitor_handle.stop()
            self._monitor_handle = None

    @staticmethod
    def get_process_metrics(name: str) -> list[tuple[int, float, float]]:
        """Retrieves resource usage for specific processes by name.

        Args:
            name: The exact name of the process.

        Returns:
            A list of tuples containing (pid, cpu_percent, ram_percent).
        """
        return _rust_monitor.get_process_metrics(name)

    @staticmethod
    def get_global_metrics() -> _rust_monitor.GlobalMetricsSnapshot:
        """Retrieves an immediate snapshot of the system's global resource usage.

        Returns:
            A GlobalMetricsSnapshot object containing detailed system metrics.
        """
        return _rust_monitor.get_global_metrics()
