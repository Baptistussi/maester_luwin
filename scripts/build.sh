#!/bin/bash
rm -rf dist && mkdir -p dist
pip install -t dist -r requirements.txt
cp -r src dist/
cd dist && zip -r ../dist/lambda.zip . -x "*.pyc" -x "__pycache__/*"
