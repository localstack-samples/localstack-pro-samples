#!/bin/bash
c=0
declare -a fail
for d in $(ls -d */); do
  cd $d
  if ! [ -e Makefile ]; then
    echo && echo SKIPPING TESTS in $d because there is no Makefile
  else
    echo && echo "Making $1 in $d" && echo
    make $1
    if [ $? != 0 ]; then
      fail[$c]=$d
      c=$((c+1))
      echo && echo "$1 in $d FAILED" && echo
      if [ $1 == test-ci ]; then
        echo && echo "LocalStack logs for $d" && echo
        cat logs.txt
      fi
    fi
  fi
cd ..
done
echo && echo && echo "TEST SUMMARY" && echo
if [ $c -gt 0 ]; then
  for f in ${fail[@]}; do
    echo "$1 FAILURE for $f"
  done
    echo && echo
  exit 1
else
echo && echo "All tests successful!" && echo
exit 0
fi
