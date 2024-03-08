#!/bin/bash
#move files to daily folders
#put and execute this script  in the general files destination
year=$(date +%Y)
month=$(date +%m)
day=$(date +%d)
month_yesterday=$(date -d '-1 day' +%m)
day_yesterday=$(date -d '-1 day' +%d)
string="$year-$month-$day"
stringYesterday="$year-$month_yesterday-$day_yesterday"
for x in *$string*.json; do 
   mv $x $string
done
for x in *$stringYesterday*.json; do 
   mv $x $stringYesterday
done




