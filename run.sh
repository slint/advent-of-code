#!/bin/bash

# First arg or current day
day=${1:-$(date +%-d)}
# Zero-pad day
day=$(printf "%02d" ${day})

# Input file is the 2nd arg or inputs/dayXX.txt
input_file=${2:-inputs/day${day}.txt}

cargo run --release --bin "day${day}" -- "${input_file}"
