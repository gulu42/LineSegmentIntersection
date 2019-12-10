#!/bin/zsh

l=(0 1 2 3 4 5 6 7 8)

for i in $l; do
    python3 frontEnd.py --inp tc_$i.txt
done
