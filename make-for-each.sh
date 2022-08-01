#!/bin/bash
#set -x
echo "invokation: $@"
echo "command: ${@:2}"
cmd=${@:2}
declare -A fail
for d in $(ls -d */); do
  cd $d
  if ! [ -e Makefile ]; then
    echo SKIPPING TESTS in $d because there is no Makefile
  else
    echo "Making $1 in $d"
    make $1 || false
    if [ $? != 0 ]; then
      fail[$d]=$d
      echo "$1 in $d FAILED" && echo
    fi

    $cmd
  fi
cd ..
done
echo && echo && echo && echo "TEST SUMMARY" && echo
if [ ${#fail[@]} -gt 0 ]; then
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
