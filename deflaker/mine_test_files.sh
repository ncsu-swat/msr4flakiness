#!/bin/bash

####
## This script assures the environment is properly configured prior to
## running mine_test_files.py.
####

## nasty bash command to obtain directory of current file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

(cd $DIR/..

 ## generating jars for Java visitors (used in mine_test_files.py)
 (cd utils/vis_ids;
  gradle build
 )
 (cd utils/vis_method;
  gradle build
 )

 ## generating virtual environment
 ./createvenv 

)

## activate virtual environment
source $DIR/../.venv/bin/activate

## run the python script
python3 mine_test_files.py
