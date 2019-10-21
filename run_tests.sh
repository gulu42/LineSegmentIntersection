#!/bin/zsh

l=(6 5 2 1 7 3 4)

for i in $l; do
    python3 frontEnd.py --inp tc_$i.txt
done
