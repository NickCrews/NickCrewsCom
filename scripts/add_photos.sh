#!/bin/bash

PHOTO_FOLDER=$1
# add trailing "/" if not present
[[ "${PHOTO_FOLDER}" != */ ]] && PHOTO_FOLDER="${PHOTO_FOLDER}/"

JSON='['
for path in "${PHOTO_FOLDER}"*; do
  # strip off everything up to last /
  name=${path##*/}
  JSON+="  {\"src\": \"$name\"},"
done
# delete the last trailing comma. sigh JSON sucks
JSON=$(echo "${JSON}" | sed '$ s/.$//')
JSON+=']'
# pretty print the JSON
echo "${JSON}" | python -m json.tool
