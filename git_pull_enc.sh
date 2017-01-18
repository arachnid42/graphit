#!/usr/bin/env bash

# USAGE
# $1 - repo branch to pull from

# checking whether necessary arguments were passed in
if [ -z "$1" ]; then
    echo ' >> no branch to pull from specified! Aborting ...'
    exit 1
fi

shopt -s nullglob  # make array to be empty when nothing has matched
read -a tmp_array <<< $(cat project_config.json | jq -r '.to_decrypt[]')
declare -a FILES_TO_DECRYPT
BRANCH=${1}

# rebuild an array of match groups into
# array of single strings
for item in "${tmp_array[@]}"; do
    for str in ${item}; do
        FILES_TO_DECRYPT[${#FILES_TO_DECRYPT[@]}]=${str}
    done
done

# getting a password from a user
read -s -p " >> enter decryption passphrase: " ENC_KEY
printf "\n"

# pulling changes
git pull origin ${BRANCH}

# decrypting sensitive data
for file in "${FILES_TO_DECRYPT[@]}"; do
    gpg --batch --yes --passphrase ${ENC_KEY} --output ${file::-4} -d ${file}
done