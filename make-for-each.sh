#!/bin/bash
#set -x
#echo "invokation: $@"
#echo "command: ${@:2}"
cmd=${@:2}
c=0
declare -a fail
for d in $(ls -d */); do
  cd $d
  if ! [ -e Makefile ]; then
    echo && echo SKIPPING TESTS in $d because there is no Makefile
  else
    echo && echo "Making $1 in $d" && echo
    make $1 || false
    if [ $? != 0 ]; then
      fail[$c]=$d
      c=$((c+1))
      echo && echo "$1 in $d FAILED" && echo
      if [ $1 == test-ci ]; then 
        echo && echo "LocalStack logs for $d" && echo
        cat logs.txt
      fi
    fi
    # TODO: do we still need an extra command, and if yes, should it be executed regargless of the make success?
    $cmd
  fi
cd ..
done
echo && echo && echo "TEST SUMMARY" && echo
if [ $c -gt 0 ]; then
  for f in ${fail[@]}; do
    echo "$1 FAILURE for $f"
  done
    echo && echo
  fi
  exit 1
else
echo && echo "All tests successful!" && echo
fi
