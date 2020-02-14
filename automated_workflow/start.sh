#!/bin/bash

apt update -y && apt upgrade -y && apt install -y curl
python3 /usr/local/automated_workflow/training/model_building.py
python3 /usr/local/automated_workflow/api/app.py &
sleep 10s
echo "API is ready to go!"