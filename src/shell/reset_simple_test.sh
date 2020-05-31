#!/bin/bash
set -x

CONTAINER="04909c27d057"

docker exec $CONTAINER tc qdisc del dev eth0 root
