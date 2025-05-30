#!/bin/bash

# Update main requirements.txt
echo "Updating requirements.txt..."
poetry export -f requirements.txt --without-hashes --output requirements.txt

# Update dev requirements.txt
echo "Updating requirements-dev.txt..."
poetry export -f requirements.txt --with dev --without-hashes --output requirements-dev.txt

echo "Requirements files updated successfully!" 