#!/bin/bash
set -x

CONTAINER="${1}"

docker exec $CONTAINER tc qdisc del dev eth0 root
