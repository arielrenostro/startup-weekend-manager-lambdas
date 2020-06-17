#!/bin/bash

LAMBDA=${1}
echo "Generating ${LAMBDA}"
./generate_zip.sh "${LAMBDA}" 2&> /dev/null
if ! [ $? -eq 0 ]
then
  echo "Error in generate_zip.sh"
  exit
fi
aws lambda update-function-code --function-name "swm-${LAMBDA}" --zip-file "fileb://./generated/${LAMBDA}.zip" | jq .LastUpdateStatus