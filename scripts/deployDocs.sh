#!/bin/bash

# package docs and deploy

DOC_PATH='./docs'
VERSION=`cat $DOC_PATH/source/conf.py | egrep 'release\s?=' | awk '{print $3}' | sed -e "s/^'//" -e "s/'$//"`
PROJECT_NAME=`cat $DOC_PATH/source/conf.py | egrep 'project\s?=' | awk '{print $3}' | sed -e "s/^'//" -e "s/'$//"`
SOURCE_FILES="$DOC_PATH/build/html/"
PACKAGE_NAME="docs_${PROJECT_NAME}_${VERSION}"


echo "building docs package $PACKAGE_NAME"

# install dev packages for doc build
pip install -e .[dev] -U tox-travis 

# make the docs from source
make docs

# package into a tar.gz file for deployment
tar -czvf "${DOC_PATH}/${PACKAGE_NAME}.tar.gz" "$SOURCE_FILES"

scp -i /tmp/dex-deploy-docs "${DOC_PATH}/${PACKAGE_NAME}.tar.gz" docs_deploy@shrimp.octet.services:
