#!/bin/bash
# Setup script for MLDS Week 1 project
# Creates virtual environment and installs dependencies

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete! Activate the virtual environment with:"
echo "  source venv/bin/activate  # On Linux/Mac"
echo "  .\\venv\\Scripts\\activate  # On Windows"
