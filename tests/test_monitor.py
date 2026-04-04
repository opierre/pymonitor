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
    cpu, brand, ram, max_ram, disk_pct, available_disk_bytes, boot = (
        monitor.get_global_metrics()
    )
    assert isinstance(cpu, float)
    assert isinstance(brand, str)
    assert isinstance(ram, float)
    assert isinstance(max_ram, int)
    assert isinstance(disk_pct, float)
    assert isinstance(available_disk_bytes, int)
    assert isinstance(boot, int)
    assert ram > 0
    assert max_ram > 0
    assert available_disk_bytes > 0
    assert boot > 0
