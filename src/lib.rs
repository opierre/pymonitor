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

/// The Rust module definition exported to Python.
#[pymodule]
fn _rust_monitor(_py: Python, module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_class::<MonitorHandle>()?;
    module.add_function(wrap_pyfunction!(get_process_metrics, module)?)?;
    Ok(())
}

define_stub_info_gatherer!(stub_info);