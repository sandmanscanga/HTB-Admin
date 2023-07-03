#!/bin/bash

# Project Path Constants
PROJECT_PATH=/opt/HTB-Admin
PROJECT_ENTRY=${PROJECT_PATH}/htb-admin.py
PROJECT_REQUIREMENTS=${PROJECT_PATH}/requirements.txt

# Virtual Environment Path Constants
VENV_PATH=${PROJECT_PATH}/venv
VENV_PYTHON=${VENV_PATH}/bin/python
VENV_ACTIVATE=${VENV_PATH}/bin/activate

# Current Path Constants
CURRENT_PATH=`pwd -P`
CURRENT_ENTRY=${CURRENT_PATH}/htb-admin.py
CURRENT_REQUIREMENTS=${CURRENT_PATH}/requirements.txt

# Runner Script Path Constant
RUNNER_PATH=/usr/local/bin/htb-admin

# Checks if user is root when running install
if [ `id -u` != 0 ]; then
    echo "[!] Must be run as root" >&2
    exit 1
fi

# Wipes old project and recreates directory
echo "[*] Wiping old project and recreating directory" &&
rm -rf $PROJECT_PATH &&
mkdir -p $PROJECT_PATH &&

# Installs a python3 virtual environment to the project path
echo "[*] Installing a python3 virtual environment to the project path" &&
python3 -m venv $VENV_PATH
if [ $? -ne 0 ]; then
    virtualenv $VENV_PATH
    if [ $? -ne 0 ]; then
        echo "[!] Failed to create Python virtual environment" >&2
        exit 2
    fi
fi

# Copy the HTB-Admin source code to the project path
echo "[*] Copying the HTB-Admin source code to the project path" &&
cp $CURRENT_ENTRY $PROJECT_PATH &&
cp $CURRENT_REQUIREMENTS $PROJECT_PATH &&

# Creating the runner script in a local system path
rm -f $RUNNER_PATH
echo '#!/bin/bash' > $RUNNER_PATH
echo "$VENV_PYTHON $PROJECT_ENTRY \$@" >> $RUNNER_PATH
chmod 755 $RUNNER_PATH

# Activate the Python virtual environment and install dependencies
echo "[*] Activating the Python virtual environment and installing dependencies" &&
source $VENV_ACTIVATE &&
pip install --upgrade pip &&
pip install -r $PROJECT_REQUIREMENTS
if [ $? -ne 0 ]; then
    echo "[!] Failed to install required packages." >&2
    exit 3
fi

# Clean up the unnecessary requirements file
echo "[*] Cleaning up the unnecessary requirements file" &&
rm -f $PROJECT_REQUIREMENTS &&
echo "[+] Finished"
