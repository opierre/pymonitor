pub mod mqtt;
pub mod victoria_metrics;

use crate::GlobalMetricsSnapshot;
use mqtt::MqttExporter;
use victoria_metrics::VictoriaMetricsExporter;

pub trait Exporter: Send {
    fn export(&mut self, metrics: &GlobalMetricsSnapshot) -> Result<(), String>;
}

pub fn create_exporter(exporter_type: &str, endpoint: &str) -> Result<Box<dyn Exporter>, String> {
    match exporter_type {
        "mqtt" => {
            let exporter = MqttExporter::new(endpoint)?;
            Ok(Box::new(exporter))
        }
        "victoriametrics" => {
            let exporter = VictoriaMetricsExporter::new(endpoint)?;
            Ok(Box::new(exporter))
        }
        _ => Err(format!("Unknown exporter type: {}", exporter_type)),
    }
}
