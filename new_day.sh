#!/bin/bash

day=$1
test_answer=$2

if [ -z "$day" ]; then
    echo "Usage: $0 <day> <test_answer>"
    exit 1
fi

mkdir -p "$day"
touch "$day/input_test.txt"
touch "$day/input.txt"

echo "TEST_ANSWER=\"$test_answer\""$'\n'"$(cat template.py)" > "$day/solution.py"
