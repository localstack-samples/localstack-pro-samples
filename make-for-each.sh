#!/bin/bash
#set -x
echo "invokation: $@"
echo "command: ${@:2}"
cmd=${@:2}
c=0
declare -a fail
for d in $(ls -d */); do
  cd $d
  if ! [ -e Makefile ]; then
    echo SKIPPING TESTS in $d because there is no Makefile
  else
    echo && echo "Making $1 in $d" && echo
    make $1 || false
    if [ $? != 0 ]; then
      fail[$c]=$d
      c=c+1
      echo "$1 in $d FAILED" && echo
    fi

    $cmd
  fi
cd ..
done
echo && echo && echo && echo "TEST SUMMARY" && echo
if [ $c -gt 0 ]; then
  for f in ${fail[@]}; do
    echo "$1 FAILURE for $f"
  done
  if [ $1 == test-ci ]; then
    echo && echo && echo "LOGS"
    for f in ${fail[@]}; do
      echo && echo "Logs for $f" && echo
      cat ${f}logs.txt
    done
    echo && echo
  fi
  exit 1
else
echo "All tests successful!"
fi
