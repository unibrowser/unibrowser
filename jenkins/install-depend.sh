#!/bin/sh
# Running inside Alpine Linux Container during build by Jenkins
echo "Installing system dependencies"
apk add --upgrade \
    python-dev \
    python3-dev \
    libxslt-dev \
    build-base \
    libxml2-dev

echo "Installing python modules"
pip install -r requirements.txt

echo "Setting up modules"
python setup.py
