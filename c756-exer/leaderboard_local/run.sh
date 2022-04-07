#!/usr/bin/env bash
# Run the service with the code for app
set -o nounset
set -o errexit

if [[ $# -gt 1  || $# == 1 && "${1}"  != "--detached" ]]
then
  echo "Usage: ${0} [--detached]"
  exit 1
fi

if [[ $# -eq 1 ]]
then
  target=run-l1-detached
else
  target=run-l1
fi

make VER=v0.25 HWD=${HWD} ${target}
