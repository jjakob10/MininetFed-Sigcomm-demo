#!/bin/bash

REQUIREMENTS_PATH=$1
OUTPUT_PATH=$2

sudo apt install python3.10-venv

python3 -m venv $OUTPUT_PATH

. $OUTPUT_PATH/bin/activate && pip install -r $REQUIREMENTS_PATH