#!/usr/bin/env bash
# Install system dependencies first
apt-get update && apt-get install -y portaudio19-dev

# Then install Python dependencies
pip install -r requirements.txt
