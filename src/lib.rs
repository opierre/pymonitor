use pyo3::prelude::*;
use sysinfo::{ProcessesToUpdate, System};
use std::thread;
use std::time::Duration;
use std::sync::{Arc, atomic::{AtomicBool, Ordering}};
use pyo3_stub_gen::{define_stub_info_gatherer, derive::{gen_stub_pyclass, gen_stub_pyfunction}};

/// Holds the shared state to allow Python to stop the Rust background thread.
#[gen_stub_pyclass]
#[pyclass]
pub struct MonitorHandle {
    is_running: Arc<AtomicBool>,
}

#[pymethods]
impl MonitorHandle {
    /// Signals the background thread to safely terminate.
    fn stop(&self) {
        self.is_running.store(false, Ordering::Relaxed);
    }
}

/// Grab usage metrics for specific processes by name.
#[gen_stub_pyfunction]
#[pyfunction]
fn get_process_metrics(name: &str) -> PyResult<Vec<(u32, f32, f32)>> {
    let mut sys = System::new_with_specifics(
        sysinfo::RefreshKind::nothing()
        .with_processes(sysinfo::ProcessRefreshKind::nothing().with_cpu().with_memory())
        .with_memory(sysinfo::MemoryRefreshKind::nothing().with_ram())
    );
    // Sleep is mandatory to establish a time delta for process CPU % calculations.
    std::thread::sleep(std::time::Duration::from_millis(200));
    sys.refresh_processes(ProcessesToUpdate::All, true);

    let mut results = Vec::new();
    let total_mem = sys.total_memory() as f32;
    for (pid, process) in sys.processes() {
        if process.name() == name {
            let mem_percent = (process.memory() as f32 / total_mem) * 100.0;
            results.push((pid.as_u32(), process.cpu_usage(), mem_percent));
        }
    }
    Ok(results)
}

#[gen_stub_pyclass]
#[pyclass(get_all)]
pub struct GlobalMetricsSnapshot {
    pub cpu_usage: f32,
    pub cpu_brand: String,
    pub ram_percent: f32,
    pub max_ram: u64,
    pub disk_percent: f32,
    pub available_disk: u64,
    pub boot_time: u64,
    pub os_name: String,
    pub os_version: String,
    pub kernel_version: String,
    pub hostname: String,
    pub core_count_physical: Option<usize>,
    pub core_count_logical: usize,
    pub cpu_temperature: Option<f32>,
    pub swap_total: u64,
    pub swap_used: u64,
    pub network_rx_bytes: u64,
    pub network_tx_bytes: u64,
    pub per_core_usage: Vec<f32>,
    pub load_avg_1m: f64,
    pub load_avg_5m: f64,
    pub load_avg_15m: f64,
}

/// Grab a single snapshot of the current global CPU, RAM usage percentage, available disk space in bytes, and boot time.
#[gen_stub_pyfunction]
#[pyfunction]
fn get_global_metrics() -> PyResult<GlobalMetricsSnapshot> {
    let mut sys = System::new_with_specifics(
        sysinfo::RefreshKind::nothing()
        .with_cpu(sysinfo::CpuRefreshKind::nothing().with_cpu_usage())
        .with_memory(sysinfo::MemoryRefreshKind::nothing().with_ram().with_swap())
    );
    let mut networks = sysinfo::Networks::new_with_refreshed_list();
    let components = sysinfo::Components::new_with_refreshed_list();
    
    sys.refresh_cpu_usage();

    // Sleep is mandatory to establish a time delta for process CPU % calculations.
    std::thread::sleep(std::time::Duration::from_millis(200));
    sys.refresh_cpu_usage();
    networks.refresh(true);

    let ram_percent = (sys.used_memory() as f32 / sys.total_memory() as f32) * 100.0;
    let cpu_brand = sys.cpus().first().map(|cpu| cpu.brand().to_string()).unwrap_or_else(|| "Unknown".to_string());

    let disks = sysinfo::Disks::new_with_refreshed_list();
    let mut available_disk_bytes = 0;
    let mut total_disk_bytes = 0;
    for disk in disks.list() {
        available_disk_bytes += disk.available_space();
        total_disk_bytes += disk.total_space();
    }

    let disk_percent = if total_disk_bytes > 0 {
        (available_disk_bytes as f32 / total_disk_bytes as f32) * 100.0
    } else {
        0.0
    };

    let os_name = System::name().unwrap_or_else(|| "Unknown".to_string());
    let os_version = System::os_version().unwrap_or_else(|| "Unknown".to_string());
    let kernel_version = System::kernel_version().unwrap_or_else(|| "Unknown".to_string());
    let hostname = System::host_name().unwrap_or_else(|| "Unknown".to_string());
    
    let core_count_physical = sysinfo::System::physical_core_count();
    let core_count_logical = sys.cpus().len();

    let mut cpu_temperature: Option<f32> = None;
    for component in &components {
        let label = component.label().to_lowercase();
        if label.contains("cpu") || label.contains("core") || label.contains("tctl") {
            cpu_temperature = component.temperature();
            break;
        }
    }

    let swap_total = sys.total_swap();
    let swap_used = sys.used_swap();

    let mut network_rx_bytes = 0;
    let mut network_tx_bytes = 0;
    for (_, data) in &networks {
        network_rx_bytes += data.received();
        network_tx_bytes += data.transmitted();
    }

    let per_core_usage: Vec<f32> = sys.cpus().iter().map(|c| c.cpu_usage()).collect();

    let load_avg = System::load_average();

    Ok(GlobalMetricsSnapshot {
        cpu_usage: sys.global_cpu_usage(),
        cpu_brand,
        ram_percent,
        max_ram: sys.total_memory(),
        disk_percent,
        available_disk: available_disk_bytes,
        boot_time: System::boot_time(),
        os_name,
        os_version,
        kernel_version,
        hostname,
        core_count_physical,
        core_count_logical,
        cpu_temperature,
        swap_total,
        swap_used,
        network_rx_bytes,
        network_tx_bytes,
        per_core_usage,
        load_avg_1m: load_avg.one,
        load_avg_5m: load_avg.five,
        load_avg_15m: load_avg.fifteen,
    })
}

/// The Rust module definition exported to Python.
#[pymodule]
fn _rust_monitor(_py: Python, module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_class::<MonitorHandle>()?;
    module.add_class::<GlobalMetricsSnapshot>()?;
    module.add_function(wrap_pyfunction!(get_process_metrics, module)?)?;
    module.add_function(wrap_pyfunction!(get_global_metrics, module)?)?;
    Ok(())
}

define_stub_info_gatherer!(stub_info);