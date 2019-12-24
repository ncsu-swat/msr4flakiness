#!/bin/bash

stat -c "%s %n" ../samples_flaky/test_cases/* | awk '{print $1}' | Rscript -e 'd<-scan("stdin", quiet=TRUE); cat(median(d))'
