"""CLI for PyMonitor."""

import platform
import subprocess
import time
from datetime import datetime

from pymonitor.monitor import PyMonitor
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typer import Option, Typer

app = Typer(help="PyMonitor CLI for tracking system constants.", add_completion=True)
console = Console()

MONITOR = PyMonitor()


@app.command()
def process(
    name: str = Option(..., "--name", "-n", help="Name of the process to monitor"),
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


def get_gpu_name() -> str:
    """Fetch GPU name via wmic on Windows or lspci on Linux."""
    try:
        if platform.system() == "Windows":
            creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
            result = subprocess.check_output(
                ["wmic", "path", "win32_VideoController", "get", "name"], text=True, creationflags=creation_flags
            )
            lines = [line.strip() for line in result.split("\n") if line.strip()]
            if len(lines) > 1:
                return lines[1]
        elif platform.system() == "Linux":
            result = subprocess.check_output(["lspci"], text=True)
            for line in result.split("\n"):
                if "VGA compatible controller" in line or "3D controller" in line:
                    parts = line.split(": ", 1)
                    if len(parts) > 1:
                        return parts[1].strip()
    except Exception:
        pass
    return "Unknown"


@app.command()
def global_metrics():
    """Fetch and display global CPU, RAM, and boot time."""
    start_time = time.perf_counter()
    cpu, cpu_brand, ram, max_ram, disk_pct, available_disk_bytes, boot_time = MONITOR.get_global_metrics()
    elapsed = time.perf_counter() - start_time

    # Fetch GPU
    gpu_brand = get_gpu_name()

    # Format into GB
    max_ram_gb = max_ram / (1024**3)
    available_disk_gb = available_disk_bytes / (1024**3)

    # Format boot time
    from datetime import timedelta

    boot_time_dt = datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S")
    uptime = timedelta(seconds=int(time.time() - boot_time))
    boot_time_display = f"{boot_time_dt} ({uptime} uptime)"

    sys_info_table = Table(show_header=False, box=None)
    sys_info_table.add_column("Property", style="cyan", justify="right")
    sys_info_table.add_column("Value", style="yellow", justify="left")

    sys_info_table.add_row("CPU:", cpu_brand)
    sys_info_table.add_row("GPU:", gpu_brand)
    sys_info_table.add_row("Total RAM:", f"{max_ram_gb:.2f} GB")
    sys_info_table.add_row("Available Disk:", f"{available_disk_gb:.2f} GB ({disk_pct:.2f}%)")
    sys_info_table.add_row("Boot Time:", boot_time_display)

    console.print(
        Panel(
            Align.center(sys_info_table),
            title=f"System Information [dim]({elapsed:.3f}s)[/dim]",
            expand=False,
            border_style="blue",
        )
    )

    table = Table(show_header=False, box=None)
    table.add_column("Metric", style="cyan", justify="right")
    table.add_column("Value", style="green", justify="left")

    table.add_row("CPU Usage:", f"{cpu:.2f}%")
    table.add_row("RAM Usage:", f"{ram:.2f}%")

    console.print(Panel(Align.center(table), title="Instant Metrics", expand=False, border_style="blue"))


if __name__ == "__main__":
    app()
