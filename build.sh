#!/bin/bash
set -e

# Use system Rust if available, otherwise install
if ! command -v rustc &> /dev/null; then
    echo "Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "Using existing Rust installation"
fi

# Set Rust environment for building
export RUST_BACKTRACE=1
export CARGO_NET_GIT_FETCH_WITH_CLI=true

# Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
