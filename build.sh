#!/bin/bash
set -e

echo "Installing Quarto..."
cd /tmp
wget -q https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.549/quarto-1.4.549-linux-amd64.tar.gz
tar -xzf quarto-1.4.549-linux-amd64.tar.gz
export PATH="/tmp/quarto-1.4.549/bin:$PATH"
cd /opt/build/repo

echo "Building site with Quarto..."
quarto render --no-clean

echo "Build complete! Files in _site:"
ls -la _site/
