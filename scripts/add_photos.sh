#!/bin/bash

JSON_PATH=../build/resources/photos_generated.json

echo [ > $JSON_PATH
for path in ../build/resources/images/photos/*; do
  # strip off everything up to last /
  name=${path##*/}
  echo $name
  echo "  {\"src\": \"$name\"}," >> $JSON_PATH
done
# delete the last trailing comma. sigh JSON sucks
sed -i '' '$ s/.$//' $JSON_PATH
echo ] >> $JSON_PATH
