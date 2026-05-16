use crate::GlobalMetricsSnapshot;
use crate::exporter::Exporter;
use std::sync::mpsc;
use std::thread;

pub struct VictoriaMetricsExporter {
    sender: mpsc::Sender<String>,
}

impl VictoriaMetricsExporter {
    pub fn new(endpoint: &str) -> Result<Self, String> {
        let (tx, rx) = mpsc::channel::<String>();
        let endpoint = endpoint.to_string();

        thread::spawn(move || {
            while let Ok(msg) = rx.recv() {
                let _ = ureq::post(&endpoint)
                    .header("Content-Type", "application/json")
                    .send(&msg);
            }
        });

        Ok(Self { sender: tx })
    }
}

impl Exporter for VictoriaMetricsExporter {
    fn export(&mut self, metrics: &GlobalMetricsSnapshot) -> Result<(), String> {
        let json = serde_json::to_string(metrics).map_err(|e| e.to_string())?;
        self.sender.send(json).map_err(|e| e.to_string())?;
        Ok(())
    }
}
