from datetime import datetime

import pytest
from typer.testing import CliRunner

from pymonitor.cli import app

runner = CliRunner()


@pytest.fixture
def mock_monitor(mocker):
    """Fixture to mock the PyMonitor instance used by the CLI."""
    monitor_mock = mocker.patch("pymonitor.cli.MONITOR")
    return monitor_mock


def test_process_command(mock_monitor):
    """Test the process CLI command with an existing process name."""
    mock_monitor.get_process_metrics.return_value = [(1234, 5.2, 15.6)]
    result = runner.invoke(app, ["process", "--name", "testproc"])
    assert result.exit_code == 0
    assert "Process Metrics: testproc" in result.stdout
    assert "1234" in result.stdout
    assert "5.20%" in result.stdout
    assert "15.60%" in result.stdout


def test_process_command_not_found(mock_monitor):
    """Test the process CLI command when no matching processes are found."""
    mock_monitor.get_process_metrics.return_value = []
    result = runner.invoke(app, ["process", "--name", "unknown"])
    assert result.exit_code == 0
    assert "No processes found" in result.stdout
    assert "unknown" in result.stdout


def test_global_metrics_command(mock_monitor):
    """Test the global-metrics CLI command."""
    mock_monitor.get_global_metrics.return_value = (
        15.5,
        "Fake CPU",
        45.2,
        32 * 1024 ** 3,
        50.0,
        12 * 1024 ** 3,
        1600000000,
    )
    result = runner.invoke(app, ["global-metrics"])
    assert result.exit_code == 0
    assert "Global System Metrics" in result.stdout
    assert "15.50%" in result.stdout
    assert "Fake CPU" in result.stdout
    assert "45.20%" in result.stdout
    assert "32.00 GB" in result.stdout
    assert "12.00 GB" in result.stdout
    assert "50.00%" in result.stdout
    expected_time = datetime.fromtimestamp(1600000000).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    assert expected_time in result.stdout
