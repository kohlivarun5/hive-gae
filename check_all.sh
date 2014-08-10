#!/bin/bash
shopt -s extglob
. ./set_path.sh 
export PYTHONPATH=$PYTHONPATH:.:./_modules/:./_libs/
pychecker --only ./_modules/Core/!(*html*).py
pychecker --only ./_modules/Social/*.py
pychecker --only ./_modules/Notify/*.py
