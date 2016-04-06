#!/bin/bash
docker-compose up -d
docker-compose -f docker-compose.yml -f docker-compose-tests.yml run --rm tests $@
