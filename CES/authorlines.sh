#!/bin/bash
echo $1
file_name=$1
line_no=`git blame --line-porcelain $1 |grep  "^author "|sort|uniq -c|sort -nr`
echo $file_name $line_no >> $2
