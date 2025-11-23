#!/bin/bash
set -e

echo "Installing Quarto..."
wget -q https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.549/quarto-1.4.549-linux-amd64.tar.gz
tar -xzf quarto-1.4.549-linux-amd64.tar.gz

echo "Building site with Quarto..."
./quarto-1.4.549/bin/quarto render

echo "Build complete! Files in _site:"
ls -la _site/
