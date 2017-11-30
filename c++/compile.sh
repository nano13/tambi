#!/usr/bin/bash

qmake-qt5 -o Makefile tambi.pro
make

if [ $? -eq 0 ]
then
    ./tambi
fi
