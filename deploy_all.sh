#!/bin/bash

LAMBDAS=("authentication" "confirm-otp" "create-pitch" "create-user" "current-phase" "list-phase" "list-pitch" "list-team" "list-user" "vote-pitch" "logout" "request-otp" "select-phase" "edit-pitch" "edit-user-photo" "get-user-photo" "next-phase" "list-team-request" "create-team-request" "confirm-team-request" "reject-team-request")

for LAMBDA in "${LAMBDAS[@]}"
do
  ./deploy.sh "${LAMBDA}"
done