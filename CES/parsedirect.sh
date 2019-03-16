#!/bin/bash
echo " parsedirect.sh <outfile>"
echo > $1
find . -type f -exec ../revlog.sh {} $1 \;
