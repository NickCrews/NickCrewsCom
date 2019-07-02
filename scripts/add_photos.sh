#!/bin/bash
export MAGICK_HOME="$HOME/Documents/software/ImageMagick-7.0.7"
export DYLD_LIBRARY_PATH="$MAGICK_HOME/lib/"
export PATH="$MAGICK_HOME/bin:$PATH"


PHOTO_FOLDER=$1
# add trailing "/" if not present
[[ "${PHOTO_FOLDER}" != */ ]] && PHOTO_FOLDER="${PHOTO_FOLDER}/"

JSON='['
for path in "${PHOTO_FOLDER}"*.jpg; do
  # strip off everything up to last /
  BNAME=$(basename ${path})
  JSON+="  {\"full\": \"${BNAME}\"},"
  # make a low-res version
  LOW_RES_DIR=$(dirname $path)"/lowres"
  mkdir -p ${LOW_RES_DIR}
  LOW_RES_PATH="${LOW_RES_DIR}/${BNAME}"
  echo ${path}
  echo ${LOW_RES_PATH}
  echo
  convert "${path}" -resize 20% "${LOW_RES_PATH}"
done
# delete the last trailing comma. sigh JSON sucks
JSON=$(echo "${JSON}" | sed '$ s/.$//')
JSON+=']'
# pretty print the JSON
# echo "${JSON}" | python -m json.tool
