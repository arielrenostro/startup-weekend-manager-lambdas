#!/bin/bash

LAMBDAS=("authentication" "confirm-otp" "create-pitch" "create-user" "current-phase" "list-phase" "list-pitch" "list-team" "list-user" "vote-pitch" "logout" "request-otp" "select-phase" "edit-pitch" "edit-user-photo" "get-user-photo")

for LAMBDA in "${LAMBDAS[@]}"
do
  ./deploy.sh "${LAMBDA}"
done