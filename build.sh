#!/bin/bash
set -e

# Install Rust to default location first
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
source ~/.cargo/env
rustup default stable

# Now set custom cargo directories for cache
export CARGO_HOME=/tmp/cargo
export CARGO_TARGET_DIR=/tmp/target
export RUST_BACKTRACE=1

# Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
