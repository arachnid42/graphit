#!/usr/bin/env bash

# USAGE
# $1 - repo branch to pull from

# checking whether necessary arguments were passed in
if [ -z "$1" ]; then
    echo ' >> no sufficient arguments to proceed! Aborting ...'
    exit 1
fi

shopt -s nullglob  # make array to be empty when nothing has matched
FILES_TO_ENCRYPT=(./app/data/*.csv ./app/data/*.json ./app/parse/mp_parser.py)
BRANCH=${1}
COMMIT_MESSAGE=${2}

# getting a password from a user
PASS_DONT_MATCH=1
while [ "${PASS_DONT_MATCH}" -eq 1 ]
 do
    read -s -p " >> enter encryption passphrase: " ENC_KEY
    printf "\n"
    read -s -p " >> repeat encryption passphrase: " ENC_KEY_VER
    printf "\n"
    if [ "${ENC_KEY}" != "${ENC_KEY_VER}" ]; then
        printf "ERROR: passwords don't match! Try again!\n"
    else
        PASS_DONT_MATCH=0
    fi
done

# encrypting sensitive data
for file in "${FILES_TO_ENCRYPT[@]}"; do
    gpg --batch --yes --passphrase ${ENC_KEY} -ac ${file}
done

# committing and pushing
git add .
git commit -m "${COMMIT_MESSAGE}"
git push origin ${BRANCH}