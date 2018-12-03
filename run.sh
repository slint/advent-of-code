#!/bin/bash

day=$1

if [ -z "$day" ]; then
    echo "Usage: $0 <PROBLEM-DAY>"
    exit 1;
fi

if [ ! -f input.txt ]; then
    echo "Download your 'input.txt' from 'https://adventofcode.com/2018/day/1/input' first!"
    exit 2
fi

python3.6 "d${day}.py"
