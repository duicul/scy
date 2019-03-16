#!/bin/bash
com_no=`git log $1 | grep -E "$commit" | wc --lines`
line_no=`cat $1 | wc --lines`
author_no=`git shortlog -s -n $1 | wc --lines`
author_most=`git shortlog -s -n $1 | head -1`
#echo $# $com_no $line_co $author_no
if [ $# -gt 1 ]
then outfile=$2
else outfile="outfilerevline.txt"
fi 
echo " $1 revision number : $com_no , lines of code : $line_no , authors : $author_no 
$author_most" >> $outfile
echo >> $outfile 
