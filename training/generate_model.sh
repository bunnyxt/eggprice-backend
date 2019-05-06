#!/bin/bash

location_name=$1
echo "Now try generate model from $location_name"

python 01_get-data-from-db.py $location_name

python 02_pretreatment.py

python 03_EEMD-LSTM.py
