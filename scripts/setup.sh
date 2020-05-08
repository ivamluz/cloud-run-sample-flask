#!/bin/bash

SCRIPT_DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $SCRIPT_DIR/..

read -p "Enter the Cloud Run Service name: " SERVICE_NAME

sed -i "s/__SERVICE_NAME__/$SERVICE_NAME/g" cloudbuild.yaml