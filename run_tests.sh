#!/bin/bash
docker-compose up -d
sleep 100
docker ps
docker-compose -f docker-compose.yml -f docker-compose-tests.yml run --rm tests $@
