#!/usr/bin/env bash

project_path=$(cd `dirname $0`; pwd)
export PYTHONPATH="${PYTHONPATH}:${project_path}"

tools/with_venv.sh python ${project_path}'/montagne/manager.py' \
    --config-file ${project_path}'/etc/montagne.conf' "$@"
