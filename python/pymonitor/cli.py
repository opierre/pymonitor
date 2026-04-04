"""CLI for PyMonitor."""
import time
from datetime import datetime

from pymonitor.monitor import PyMonitor
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
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
    metrics = MONITOR.get_process_metrics(name)
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


@app.command()
def global_metrics():
    """Fetch and display global CPU, RAM, and boot time."""
    start_time = time.perf_counter()
    cpu, cpu_brand, ram, max_ram, disk_pct, available_disk_bytes, boot_time= MONITOR.get_global_metrics()
    elapsed = time.perf_counter() - start_time

    # Format into GB
    max_ram_gb = max_ram / (1024**3)
    available_disk_gb = available_disk_bytes / (1024**3)

    # Format boot time
    boot_time_dt = datetime.fromtimestamp(boot_time).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    table = Table(
        title=f"Global System Metrics [dim]({elapsed:.3f}s)[/dim]",
        show_header=True,
        header_style="bold magenta",
        title_justify="center",
    )
    table.add_column("Metric", style="cyan", justify="left")
    table.add_column("Value", style="green", justify="right")
    table.add_column("Reference", style="yellow", justify="right")

    table.add_row("CPU Usage (%)", f"{cpu:.2f}%", cpu_brand)
    table.add_row("RAM Usage (%)", f"{ram:.2f}%", f"{max_ram_gb:.2f} GB")
    table.add_row("Available Disk (%)", f"{disk_pct:.2f}%", f"{available_disk_gb:.2f} GB")
    table.add_row("Boot Time", f"{boot_time_dt}", "-")

    panel = Panel(Align.center(table), expand=False, border_style="blue")
    console.print(panel)


if __name__ == "__main__":
    app()
