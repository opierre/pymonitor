# PyMonitor

A highly optimized system resource monitor.</br> 
This package pushes the infinite polling loops and 
network transmission down into compiled Rust code to achieve a near-zero CPU footprint, 
while providing a clean easy-to-use Python interface.

***

## Quickstart: compiling Rust via Python Build

This project relies on `uv` for lightning-fast virtual environment management and `maturin` as the build-backend to 
compile the Rust extension seamlessly.

### 1. Install Dependencies

Ensure you have the Rust compiler (`rustup`) installed. Then, [install `uv`](https://docs.astral.sh/uv/getting-started/installation/).

### 2. Build and Install

Run the following commands to create a virtual environment, compile the Rust code, and install the Python package 
dynamically:

```bash
uv venv
source .venv/bin/activate
uv pip install -e .[dev]
```

Under the hood, uv detects maturin in [pyproject.toml](pyproject.toml), compiles src/lib.rs, and links the resulting shared object 
file into local Python environment.

### 3. Run Formatting, Linting and Tests

```bash
ruff format .
ruff check .
pytest
```

***