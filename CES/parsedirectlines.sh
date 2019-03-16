#!/bin/bash
echo " authorlines.sh <outfile>"
echo > $1
find . -type f -exec ../authorlines.sh {} $1 \;
