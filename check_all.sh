#!/bin/bash
shopt -s extglob
. ./set_path.sh 
pychecker --only modules/Core/!(*html*).py
pychecker --only modules/Social/*.py
