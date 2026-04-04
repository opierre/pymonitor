use pyo3_stub_gen::Result;

fn main() -> Result<()> {
    // Call the generated stub function from library (src/lib.rs)
    let stub_info = _rust_monitor::stub_info()?;

    // Generate the .pyi file in the root of project
    stub_info.generate()?;

    println!("Successfully generated stubs!");

    Ok(())
}