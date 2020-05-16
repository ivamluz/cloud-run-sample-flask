#!/bin/bash

read -p "Enter the Cloud Run Service name: " SERVICE_NAME
read -s -p "Enter the API KEY: " API_KEY

HASHED_API_KEY=`./hash_value.py --value "${API_KEY}"`

gcloud run \
  services update $SERVICE_NAME \
  --region us-central1 \
  --platform managed \
  --update-env-vars HASHED_API_KEY=$HASHED_API_KEY