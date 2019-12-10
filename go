#!/bin/bash

if [ "$1" == "-h" ]; then
  echo "usage: go [day [year]]"
  echo "if no year specified, use current/most recent aoc"
  echo "if no day specified, start first unworked problem, or most recent"
  exit
fi

day=$1
last_year=`if [ $(date +%m) -eq 12 ]; then date +%Y; else expr $(date +%Y) - 1; fi`

if [ "$day" == "" ]; then
  year=2015
  day=1
  file=
  while [ -f "$year/$(printf "%02d" $day).py" ]
  do
    ((++day))
    if [ $day -gt 25 ]; then
      day=1
      ((++year))
    fi
    if [ $day -eq 25 ] && [ $year -eq $last_year ]; then
      break
    fi
  done
else
  year=${2:-$last_year}
fi

file=$year/$(printf "%02d" $day).py
inputfile=$year/input$(printf "%02d" $day).py

if [ ! -f "$inputfile" ]; then
  ./get $day $year
  if [ $? -ne 0 ]; then
    exit 1
  fi
fi

if [ ! -f "$file" ]; then
  echo "from input$(printf "%02d" $day) import v" > $file
  echo "" >> $file
  echo "v = v.strip()" >> $file
fi

$EDITOR $file
