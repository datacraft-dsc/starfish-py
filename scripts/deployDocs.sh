#!/bin/bash

# package docs and deploy

make docs
DOC_PATH='./docs'
VERSION=`cat $DOC_PATH/source/conf.py | egrep 'release\s?=' | awk '{print $3}' | sed -e "s/^'//" -e "s/'$//"`
PROJECT_NAME=`cat $DOC_PATH/source/conf.py | egrep 'project\s?=' | awk '{print $3}' | sed -e "s/^'//" -e "s/'$//"`
SOURCE_FILES="$DOC_PATH/build/html/"
PACKAGE_NAME="docs_${PROJECT_NAME}_${VERSION}"

echo "building package $PACKAGE_NAME"
tar -czvf "${DOC_PATH}/${PACKAGE_NAME}.tar.gz" "$SOURCE_FILES"
