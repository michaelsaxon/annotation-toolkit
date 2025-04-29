#!/bin/bash

# Exit on error
set -e

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
pip install gunicorn

# Create responses directory if it doesn't exist
mkdir -p responses

# Copy service file to systemd directory
echo "Installing systemd service..."
sudo cp hilite-webform.service /etc/systemd/system/

# Reload systemd
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable and start the service
echo "Enabling and starting the service..."
sudo systemctl enable hilite-webform
sudo systemctl start hilite-webform

# Check service status
echo "Checking service status..."
sudo systemctl status hilite-webform

echo "Setup complete! The Hilite Webform service should now be running."
echo "You can check its status with: sudo systemctl status hilite-webform"
echo "You can view logs with: sudo journalctl -u hilite-webform" 