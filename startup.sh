#!/usr/bin/env bash

# custom output colors
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`

echo "${GREEN}>> running project setup ...${RESET}"

# running sass compiler in the background
echo "${GREEN}>> starting up sass compiler in background ...${RESET}"
sass_input_folder=$(cat config.json | jq -r '.sass_in')
sass_output_folder=$(cat config.json | jq -r '.sass_out')
nohup sass --watch ${sass_input_folder}:${sass_output_folder} &

# starting flask to run the whole project
echo "${GREEN}>> starting up the web server ...${RESET}"
./flask_init.py