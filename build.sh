#!/bin/bash
set -e

docker build --network="host" --tag pyserver .
echo "Dockerfile built."
