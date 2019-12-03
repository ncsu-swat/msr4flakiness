#!/bin/bash

count() {
    PARAM=$1 
    echo -n "$PARAM " & grep -rni "$PARAM" test_tokens/* | wc -l      
}


count time
count call
count wait
count host
count thread
count sleep
count join
count receive
count task
count send
count concur
count sync
