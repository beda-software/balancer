#!/bin/bash
docker kill `docker ps | grep bedasoftware/hello-world | awk '{print $1}'`
docker rm  `docker ps -a | grep bedasoftware/hello-world | awk '{print $1}'`
docker-compose kill && docker-compose down
