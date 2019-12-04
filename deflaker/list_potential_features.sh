#!/bin/bash

count() {
    PARAM=$1 
    echo -n "$PARAM " & grep -rni "$PARAM" test_tokens/* | wc -l      
}


count action ## mostly oozie
count file
count service
count time
count start
count execut
count call
count wait
count close
count url
count connect
count message
count host
count thread
count shutdown
count sleep
count http
count open
count join
count receive
count task
count send
count concur
count sync
count finish
count expire
count flush
count transaction
