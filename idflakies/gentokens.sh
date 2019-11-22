#!/bin/bash

(cd vis_ids;
 gradle build
)

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
JAR=$DIR/vis_ids/build/libs/vis_ids.jar

for x in `ls tests/*`
do
    FILENAME=$DIR/tests_tokens/$(basename $x)
    echo $FILENAME
    java -jar $JAR $DIR/$x > $FILENAME
done
