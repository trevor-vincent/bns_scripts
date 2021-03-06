#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "find_segment_at_time.sh <TIME_TO_GREP_FOR>"
    echo "You can grep for a partial time such as 39 instead of the full time 3900 to maximize results, the time should be in simulation units"
exit
fi

echo $1
find $PWD -name "SpEC.out" | sort -k2 | while read line;
do

output=$(cat $line | grep CPU | grep "CpuUsage"  | cut -d ',' -f 1 | grep "$1")
if [ ! "$output" == "" ]; then
    echo $line
    cat $line | grep CPU | grep "CpuUsage" | grep "$1"
fi
done
