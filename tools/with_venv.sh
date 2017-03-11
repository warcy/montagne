#!/bin/sh

TOOLS=`dirname $0`
VENV=$TOOLS/../.venv
. $VENV/bin/activate && $@
