#!/bin/bash

# Setup script for RAT tool

echo "Setting up Remote Support Tool..."

# Create directories
mkdir -p $HOME/remote_support/logs

# Generate SSL certificates
echo "Generating SSL certificates..."
openssl req -x509 -newkey rsa:2048 \
  -keyout $HOME/remote_support/key.pem \
  -out $HOME/remote_support/cert.pem \
  -days 365 -nodes -subj "/CN=localhost"

echo "✓ Setup complete!"
echo ""
echo "Run server: REMOTE_TOKEN=\"your-token\" python server.py"
echo "Run agent: REMOTE_TOKEN=\"your-token\" REMOTE_HOST=\"127.0.0.1\" python agent.py"
