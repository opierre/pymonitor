from pymonitor.cli import app
import pytest
from typer.testing import CliRunner

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

