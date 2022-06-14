#!/bin/bash

# Project Path Constants
PROJECT_PATH=/opt/HTB-Admin

# Runner Script Path Constant
RUNNER_PATH=/usr/local/bin/htb-admin

# Checks if user is root when running install
if [ `id -u` != 0 ]; then
    echo "[!] Must be run as root" >&2
    exit 1
fi

# Wipes old project and runner script
echo "[*] Wiping old project and recreating directory" &&
rm -rf $PROJECT_PATH &&
rm -f $RUNNER_PATH &&
