#!/bin/sh

export OS_TENANT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=cipc
export OS_AUTH_URL=http://192.168.1.210:35357/v2.0

TOOLS=`dirname $0`
VENV=$TOOLS/../.venv
. $VENV/bin/activate && $@
