#!/bin/bash
#set -e

SCRIPT_DIR=`dirname $0`
DEVELOP_ENV=$SCRIPT_DIR/env_develop

find . -name *pyc* -delete
trap "pkill -f snmpsimd.py; exit" SIGHUP SIGINT SIGTERM

${VIRTUAL_ENV}/bin/python ${VIRTUAL_ENV}/bin/snmpsimd.py --v2c-arch --agent-port=1161 --device-dir=integration_tests/snmpsim/simulated_data/ --validate-device-data &

nosetests $INTEGRATION_TESTS -s --logging-clear-handlers --processes=16 --process-timeout=20
RETCODE=$?

pkill -f snmpsimd.py
sleep 1
exit $RETCODE

find . -name *pyc* -delete
