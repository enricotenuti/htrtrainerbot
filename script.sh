#!/bin/bash

output_file="output.txt"

for i in {1..1000}
do
    nissy scramble dr | tee -a "$output_file"
done