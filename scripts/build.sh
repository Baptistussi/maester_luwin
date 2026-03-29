#!/bin/bash
mkdir -p dist
pip install -t dist -r requirements.txt
cp -r keys dist/
cd src && zip -r ../dist/cronjob.zip . -x "*.pyc" -x "__pycache__/*"
