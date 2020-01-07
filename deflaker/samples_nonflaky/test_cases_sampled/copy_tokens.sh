#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

for x in $DIR/*
do
    NAME=$(basename $x)
    cp $DIR/../test_tokens/$NAME $DIR/tokens/.
done

     
