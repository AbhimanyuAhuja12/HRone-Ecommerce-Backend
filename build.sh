#!/bin/bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env
rustup default stable

# Set Cargo environment variables
export CARGO_HOME=/tmp/cargo
export RUSTUP_HOME=/tmp/rustup

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
