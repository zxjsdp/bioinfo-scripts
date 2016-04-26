#!/bin/bash

# This script is for jdock computing with multiprocessing.

if [ $UID -ne 0 ]; then
    echo "ERROR: Superuser privileges are required to run this script."
    echo "e.g. \"sudo $0\""
    exit 1
fi


sudo python _multiprocessing_dock_in.py
