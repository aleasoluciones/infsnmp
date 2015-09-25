#!/bin/bash
#set -e

nosetests integration_tests -s --logging-clear-handlers --processes=16 --process-timeout=20
