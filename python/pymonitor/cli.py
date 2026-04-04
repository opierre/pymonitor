"""CLI for PyMonitor."""
import time

from pymonitor.monitor import PyMonitor
from rich.console import Console
from rich.table import Table
from typer import Option, Typer

app = Typer(
     help="PyMonitor CLI for tracking system constants.",
     add_completion=True
)
console = Console()

MONITOR = PyMonitor()

@app.command()
def process(
    name: str = Option(
    ..., "--name", "-n", help="Name of the process to monitor"
    ),
):
    """Fetch and display metrics for a specific process."""
    start_time = time.perf_counter()
    metrics = MONITOR.get_process_mess_metrics(name)
    elapsed = time.perf_counter() - start_time

    if not metrics:
        console.print(f"[bold red]No processes found with name:[/bold red] '{name}'")
        return

    table = Table(
        title=f"Process Metrics: {name} [dim]({elapsed:.3f}s)[/dim]",
        show_header=True,
        header_style="bold magenta",
        title_justify="center",
    )
    table.add_column("PID", style="cyan", justify="center")
    table.add_column("CPU Usage (%)", style="green", justify="right")
    table.add_column("RAM Usage (%)", style="yellow", justify="right")

    for pid, cpu, mem in metrics:
        table.add_row(str(pid), f"{cpu:.2f}%", f"{mem:.2f}%")

    console.print(table)


if __name__ == "__main__":
    app()
