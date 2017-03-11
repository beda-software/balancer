#!/bin/bash
docker-compose up -d
docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm wait_for
docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm tests $@
