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
    mock_monitor.get_process_mess_metrics.return_value = [(1234, 5.2, 15.6)]
    result = runner.invoke(app, ["--name", "testproc"])
    assert result.exit_code == 0
    assert "Process Metrics: testproc" in result.stdout
    assert "1234" in result.stdout
    assert "5.20%" in result.stdout
    assert "15.60%" in result.stdout
