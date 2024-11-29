#!/bin/bash
set -e

# This script should not be run manually
# It is intended to be run automatically by the service dependency-installer of the docker compose for local development puspouses
# It will install the dependencies in the lib folder and create a hash file to avoid reinstalling them if they are already installed

hash=$(md5sum requirements.txt | awk '{ print $1 }')
if [ ! -f lib/requirements.txt.hash ] || [ "$hash" != "$(cat lib/requirements.txt.hash)" ]; then
    echo "Removing old dependencies..."
    rm -rf lib/*
    echo "Installing dependencies..."
    pip install -r requirements.txt -t lib
    echo "Installing debug lib..."
    pip install pydevd-pycharm==241.19072.16 --no-cache-dir --no-binary=pydevd-pycharm -t lib
    echo $hash > lib/requirements.txt.hash
else
    echo "Dependencies already installed"
    exit 0
fi
