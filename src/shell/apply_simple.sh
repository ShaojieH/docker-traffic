#!/bin/bash
set -x

CONTAINER="${1}"
DST_IP="${2}"
LIMIT="${3}"
PRIO="${4}"

docker exec $CONTAINER tc qdisc add dev eth0 root handle 1: htb default 12
docker exec $CONTAINER tc class add dev eth0 parent 1: classid 1:1 htb rate "$LIMIT"kbps ceil "$LIMIT"kbps prio $PRIO
docker exec $CONTAINER tc filter add dev eth0 parent 1: protocol ip prio 16 u32 match ip dst $DST_IP flowid 1:1
