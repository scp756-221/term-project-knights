#!/usr/bin/env bash
docker container run --rm \
  -v ${PWD}/gatling/results:/opt/gatling/results \
  -v ${PWD}/gatling:/opt/gatling/user-files \
  -v ${PWD}/gatling/target:/opt/gatling/target \
  -e CLUSTER_IP='44.238.226.5' \
  -e USERS=1 \
  -e SIM_NAME=WriteTableSim \
  --label gatling \
  ghcr.io/scp-2021-jan-cmpt-756/gatling:3.4.2 \
  -s proj756.WriteTableSim