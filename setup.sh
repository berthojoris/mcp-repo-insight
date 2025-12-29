#!/bin/bash

echo "========================================"
echo "RepoInsight MCP - Quick Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

echo "[1/4] Checking Python version..."
python3 --version

echo ""
echo "[2/4] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "Virtual environment created"
fi

echo ""
echo "[3/4] Activating virtual environment..."
source venv/bin/activate

echo ""
echo "[4/4] Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the server:"
echo "  1. Activate environment: source venv/bin/activate"
echo "  2. Run server: python -m repoinsight_mcp.main"
echo ""
echo "To use with Claude Desktop:"
echo "  1. Edit: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "  2. Add configuration from mcp_config_example.json"
echo "  3. Update paths to match your installation"
echo ""
echo "For more details, see SETUP.md"
echo ""
