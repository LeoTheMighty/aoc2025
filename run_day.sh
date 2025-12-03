#!/bin/bash

day=$1

if [ -z "$day" ]; then
    # find latest day (alphabetical directory)
    day=$(ls -d day* | sort -r | head -n 1)
fi

cd $day
echo "Running day $day"
python solution.py
cd ..
