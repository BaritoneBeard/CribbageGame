#!/bin/bash
set -e

docker build --network="host" --tag pyserver .
echo "Dockerfile built."
docker run --network="host"  -p 5000:5000 -d pyserver
