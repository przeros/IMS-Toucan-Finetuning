#!/bin/bash

# 1. Run the git pull command
echo "Running git pull..."
git pull

# 2. Recursively delete all files except 'dataset' from the directory '../Dataset'
echo "Recursively cleaning up ../Dataset directory..."
find ../Dataset -type f ! -name 'dataset' -delete
find ../Dataset -type d ! -name 'dataset' ! -name 'Dataset' -exec rm -rf {} +

# 3. Run the Python script with the specified parameters
echo "Running the training pipeline..."
python3 run_training_pipeline.py fine_ex --gpu_id GPU-7c1e3e22-8e79-6a5a-9963-edcbbcc6af20

echo "Script execution completed."
