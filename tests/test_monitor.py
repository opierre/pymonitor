from python.pymonitor.monitor import PyMonitor


def test_get_process_mess_metrics() -> None:
    """Test that the Rust backend returns process metrics."""
    monitor = PyMonitor()
    processes = monitor.get_process_metrics("python")
    assert isinstance(processes, list)
    for process in processes:
        assert isinstance(process, tuple)
        assert len(process) == 3
