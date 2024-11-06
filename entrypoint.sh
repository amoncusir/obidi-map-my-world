#!/bin/sh

set -x

# Function to run the API
run_api() {
  echo "Starting API with arguments: $@"
  uvicorn "$@" 'src.app.api_instance:api'
}

# Check if at least one argument is provided
if [ -z "$1" ]; then
  echo "You must provide the <mode> argument"
  exit 1
fi

# Capture the first argument as the mode to run
mode=$1
shift # Remove the first argument to pass the remaining arguments

# Execute the corresponding function based on the first argument
case "$mode" in
  api)
    run_api "$@"
    ;;
  *)
    echo "Invalid option. Use 'api',"
    exit 1
    ;;
esac
