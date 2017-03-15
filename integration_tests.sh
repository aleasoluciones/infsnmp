#!/bin/bash
set -e

trap "pkill -f snmpsimd.py; exit" SIGHUP SIGINT SIGTERM
python $(which snmpsimd.py) --v2c-arch --agent-port=1161 --device-dir=integration_tests/snmpsim/simulated_data/ --validate-device-data 2>/dev/null 1>/dev/null &
nosetests $INTEGRATION_TESTS -s --logging-clear-handlers --processes=16 --process-timeout=50 --with-yanc
NOSE_RETCODE=$?
exit $NOSE_RETCODE