#!/usr/bin/env bash

# custom output colors
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`

echo "${GREEN}>> running project bootstrap script ...${RESET}"
# starting flask to run the whole project
echo "${GREEN}>> starting up the web server ...${RESET}"
./flask_init.py
