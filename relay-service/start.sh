#!/bin/bash
set -e

function run_app() {
  echo "Starting main application..."
  if ! uvicorn relay_service.app:app --host 0.0.0.0 --port 8000; then
    echo "Application failed. Sleeping for 6 mins to allow debugging..."
    sleep 360
    exit 1
  fi
}

case "$1" in
  app)
    run_app
    ;;
  "")
    run_app
    ;;
  *)
    echo "Unknown argument: $1"
    echo "Usage: $0 [app]"
    exit 1
    ;;
esac
