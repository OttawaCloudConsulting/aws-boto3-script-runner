#!/bin/bash

# Ensure the necessary environment variables are set
if [ -z "$PYTHON_FILE" ] || [ -z "$REQUIREMENTS_FILE" ]; then
  echo "Error: PYTHON_FILE and REQUIREMENTS_FILE environment variables must be set."
  exit 1
fi

# Install dependencies from the specified requirements file
pip install -r "$REQUIREMENTS_FILE"

# Execute the specified Python file
python "$PYTHON_FILE"
