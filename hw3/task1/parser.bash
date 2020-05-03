#!/bin/bash

function count_overall() {
  printf '***** OVERALL COUNT OF REQUESTS *****\n\n'
  wc -l <"$log"
  printf '\n'
}

function count_by_type() {
  printf '***** REQUESTS COUNT BY TYPE *****\n\n'
  cat "$log" | tr '"' ' ' | tr -s ' ' | cut -d' ' -f6 | sort | uniq -c | awk '{print $2 " " $1}' | column -t
  printf '\n'
}

function top10_size() {
  printf '***** TOP 10 REQUESTS BY SIZE *****\n\n'
  cat "$log" | tr '"' ' ' | awk '{print $7, $9, $10}' | sort -r -n -k3 | uniq -c | sort -r -n -k4 |
    head -n 10 | column -t
  printf '\n'
}

function top10_400() {
  printf '***** TOP 10 REQUESTS WITH CLIENT ERRORS *****\n\n'
  cat "$log" | tr '"' ' ' | awk 'match($9, /^4[[:digit:]]+$/) {print $1, $6, $7, $9}' | sort -n -k1 | uniq -c |
    sort -r -k1 | head -n 10 | column -t
  printf '\n'
}

function top10_300() {
  printf '***** TOP 10 REQUESTS WITH REDIRECTS *****\n\n'
  cat "$log" | tr '"' ' ' | awk 'match($9, /^3[[:digit:]]+$/) {print $1, $6, $7, $9}' | sort -n -k1 | uniq -c |
    sort -r -k1 | head -n 10 | column -t
  printf '\n'
}

if [[ $# == 0 ]]; then
  echo "Error: expected 1 or more arguments; got $#"
  echo "use -h for help"
  exit 1
elif [[ "$1" == '-h' ]]; then
  echo 'Script to parse nginx logs'
  echo '-c to count all requests'
  echo '-t to count methods'
  echo '-s to show top 10 requests by size of package'
  echo '-e to show top 10 requests with client errors'
  echo '-r to show top 10 requests with redirects'
  exit 1
else
  log=$(find "${@: -1}" -maxdepth 1 -name access.log 2>/tmp/Error)
  ERROR=$(</tmp/Error)
  if [[ -n $ERROR ]]; then
    echo 'Invalid filename'
    exit 1
  fi
fi

while getopts ":ctserh" opt; do
  case $opt in
  # COUNT REQUESTS (c)
  c)
    count_overall
    ;;
  # COUNT REQUESTS BY TYPE (t)
  t)
    count_by_type
    ;;
  # TOP 10 LARGEST BY SIZE (s)
  s)
    top10_size
    ;;
  # TOP 10 40* REQUESTS (e)
  e)
    top10_400
    ;;
  # TOP 10 30* REQUESTS (r)
  r)
    top10_300
    ;;
  h) ;;
  *)
    echo "Invalid option"
    ;;
  esac
done

if [[ $OPTIND == 1 ]]; then
  count_overall
  count_by_type
  top10_size
  top10_400
  top10_300
fi
