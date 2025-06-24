#!/bin/bash

echo "Installing Python dependencies for PrepMe..."

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required libraries
pip install \
  pandas \
  requests \
  beautifulsoup4 \
  selenium \
  webdriver-manager \
  langchain \
  langchain-community \
  langchain-core \
  langchain-groq \
  openai \
  tiktoken

echo "All dependencies installed successfully!"
