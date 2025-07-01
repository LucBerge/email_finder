#!/bin/bash

cd ..
mkdir data
echo "Installing virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Ready to use!"
