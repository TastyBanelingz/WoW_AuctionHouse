#!/bin/bash
# My first script
echo "Starting Data Cleaning..."
lua GetData.lua
echo "Data retrieved from LUA files. Cleaning Data..."
python3 ProcessData.py
echo "Data clean and added to SQL DB."
echo "Done"
