#!/bin/bash

day=${1}
lang=${2}
input_file=${3:-inputs/day${1}.txt}

# Rust 
echo "# Rust"
[[ $lang == "rust" ]] && cargo run --manifest-path "rust/Cargo.toml" --bin "day${day}" -- "${input_file}"
echo

# JavaScript
echo "# JavaScript"
[[ $lang == "js" ]] && node "js/day${day}.js" "${input_file}"
echo

# Python
echo "# Python"
[[ $lang == "py" ]] && env python "python/day${day}.py" "${input_file}"
echo
