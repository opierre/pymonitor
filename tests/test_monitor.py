from python.pymonitor.monitor import PyMonitor


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
