#!/bin/bash
#set -e

docker build -t snmpd .
docker run --rm -p 1161:161/udp --name snmpd -t snmpd &
nosetests integration_tests -s --logging-clear-handlers --processes=16 --process-timeout=20
docker stop snmpd



