#!/bin/bash

# Dummy status test
CMD="ps aux | grep '[p]ython'"

echo "boss: " $(ssh boss "$CMD")
echo "emp1: " $(ssh pi@emp1 "$CMD")
echo "emp2: " $(ssh pi@emp2 "$CMD")
echo "emp3: " $(ssh pi@emp3 "$CMD")
