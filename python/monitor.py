"""A lightweight monitor for computer constants."""


class PyMonitor:
    """A lightweight monitor for computer constants.

    This class provides a Python interface to the Rust-based
    system monitoring tools. It should allow for background polling
    and pushing data directly to a database.
    """

    def __init__(self, database_url: str, interval: int = 5):
        """Initialize PyMonitor instance.

        Args:
            database_url: database HTTP endpoint URL.
            interval: polling interval in seconds. Defaults to 5.
        """
        # Store instance attributes
        self._db_url = database_url
        self._interval = interval
        self._monitor_handle = None

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

