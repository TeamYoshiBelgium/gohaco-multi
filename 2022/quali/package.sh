#!/bin/sh

set -x

ORIG_DIR=$(pwd)
DIR="$( cd "$( dirname "$0" )" && pwd -P)"
cd $DIR/..
rm -f  package.zip
zip -r package.zip $DIR -x $DIR/out
cd $ORIG_DIR