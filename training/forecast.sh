#!/bin/bash

location_name=$1
echo "Now try forecast price from $location_name"

echo "01: get data from db"
python 01_get-data-from-db.py $location_name

echo "02: pre treatment"
python 02_pre-treatment.py

echo "03: do EEMD-LSTM forecast"
python 03_EEMD-LSTM.py

echo "04: store forecast result to db"
# python 04_store-forecast-result-to-db.py $location_name

echo "remove data.csv and result.txt"
# rm data.csv
# rm result.txt

echo "Finish forecast price from $location_name"