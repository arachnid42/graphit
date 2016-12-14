#!/usr/bin/env bash

# USAGE
# $1 - key to use for encryption
# $2 - repo branch to push to
# $3 - message to commit with

# checking whether necessary arguments were passed in
if [ -z "$1" ] || [ -z "$2" ]; then
    echo ' >> no sufficient arguments to proceed! Aborting ...'
    exit 1
fi

shopt -s nullglob  # make array to be empty when nothing has matched
FILES_TO_ENCRYPT=(./app/backup/*.pkl ./app/data/*.csv ./app/parse/mp_parser.py)

# assigning variables
ENC_KEY=${1}
BRANCH=${2}

# encrypting sensitive data
for file in "${FILES_TO_ENCRYPT[@]}"; do
    gpg --batch --yes --passphrase ${1} -ac ${file}
done

# committing and pushing
git add .
git commit -m "${3}"
git push origin ${2}