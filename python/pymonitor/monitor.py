"""A lightweight monitor for computer constants."""
from . import _rust_monitor


class PyMonitor:
    """A lightweight monitor for computer constants.

    This class provides a Python interface to the Rust-based
    system monitoring tools. It should allow for background polling
    and pushing data directly to a database.
    """

    def __init__(self, database_url: str | None = None, interval: int = 5):
        """Initialize PyMonitor instance.

        Args:
            database_url: database HTTP endpoint URL.
            interval: polling interval in seconds. Defaults to 5.
        """
        # Store instance attributes
        self._db_url = database_url
        self._interval = interval
        self._monitor_handle: _rust_monitor.MonitorHandle | None = None

    def start(self) -> None:
        """Starts the background Rust monitoring thread.

        Raises:
            RuntimeError: if the monitor is already actively running.
        """
        if self._monitor_handle is not None:
            raise RuntimeError("Monitor is already running.")
        # TODO: start monitoring thread

    def stop(self) -> None:
        """Stops the background Rust monitoring thread."""
        if self._monitor_handle is not None:
            # TODO: stop the thread
            pass

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
    def get_global_metrics() -> tuple[float, str, float, int, float, int, int]:
        """Retrieves an immediate snapshot of the system's global resource usage.

        Returns:
            A tuple of (cpu_usage_percentage, cpu_brand, ram_percent, max_ram, disk_percent, available_disk,
            boot_time).
        """
        return _rust_monitor.get_global_metrics()
