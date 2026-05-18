#!/bin/bash

# Simple script to check if Airflow is up by querying the health endpoint

echo "Checking Airflow webserver health..."

# We loop up to 30 times, waiting 5 seconds between checks.
for i in {1..30}; do
  # curl the health endpoint. We use -s to silence the progress bar and -f to fail silently on server errors
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health)

  if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "Airflow webserver is UP and healthy!"
    exit 0
  fi

  echo "Waiting for Airflow webserver to start... (Attempt $i/30)"
  sleep 5
done

echo "Airflow webserver failed to start or become healthy within the expected time."
exit 1
