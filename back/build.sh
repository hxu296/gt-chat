#!/bin/bash
pip3 install -r requirements.txt
pip3 install --upgrade gdown
mkdir -p search_index
gdown -O search_index/ https://drive.google.com/uc?id=1N1TgnfOWrylVqVv45Z-g06i-Wy4S81J_
gdown -O search_index/ https://drive.google.com/uc?id=1VOgUuBrkOO2E14XgJ1kJDGq5_pGdCSAy