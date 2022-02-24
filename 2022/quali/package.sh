#!/bin/sh

set -x

ORIG_DIR=$(pwd)
DIR="$( cd "$( dirname "$0" )" && pwd -P)"
cd $DIR/..
rm -f package.zip
zip package.zip "$DIR/classes"* "$DIR/"*

cd $ORIG_DIR