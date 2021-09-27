#!/bin/bash
set -e

docker build --tag docker-gs-ping .
echo "Dockerfile built."
