#!/bin/bash
mkdir -p dist
pip install -t dist -r requirements.txt
cd src && zip -r ../dist/cronjob.zip . -x "*.pyc" -x "__pycache__/*"
