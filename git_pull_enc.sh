#!/usr/bin/env bash

# USAGE
# $1 - repo branch to pull from

# checking whether necessary arguments were passed in
if [ -z "$1" ]; then
    echo ' >> no branch to pull from specified! Aborting ...'
    exit 1
fi

shopt -s nullglob  # make array to be empty when nothing has matched
FILES_TO_ENCRYPT=$(echo $(cat project_config.json | jq -r '.to_encrypt') | sed 's/ /\.asc /g')
FILES_TO_ENCRYPT+=".asc"
BRANCH=${1}

# getting a password from a user
read -s -p " >> enter decryption passphrase: " ENC_KEY
printf "\n"

# pulling changes
git pull origin ${BRANCH}

# decrypting sensitive data
for file in "${FILES_TO_ENCRYPT[@]}"; do
    echo ${ENC_KEY}
    echo ${file::-4}
    echo ${file}
    gpg --batch --yes --passphrase ${ENC_KEY} --output ${file::-4} -d ${file}
done