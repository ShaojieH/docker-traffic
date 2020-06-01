#!/bin/bash
set -x

CONTAINER="6d5fc7c4961a"
DEV="eth0"
WORKER1="172.18.0.5"
WORKER2="172.18.0.3"
WORKER3="172.18.0.4"

docker exec $CONTAINER tc qdisc del dev $DEV root

# first group
docker exec $CONTAINER tc qdisc add dev $DEV root handle 1: htb default 12
docker exec $CONTAINER tc class add dev $DEV parent 1: classid 1:1 htb rate 8000kbps ceil 8000kbps

docker exec $CONTAINER tc class add dev $DEV parent 1:1 classid 1:10 htb rate 6000kbps ceil 6000kbps
docker exec $CONTAINER tc class add dev $DEV parent 1:1 classid 1:11 htb rate 1000kbps ceil 1000kbps
docker exec $CONTAINER tc class add dev $DEV parent 1:1 classid 1:12 htb rate 8000kbps ceil 8000kbps

docker exec $CONTAINER tc filter add dev $DEV protocol ip parent 1:0 prio 1 u32 \
   match ip dst $WORKER1 flowid 1:10
docker exec $CONTAINER tc filter add dev $DEV protocol ip parent 1:0 prio 1 u32 \
   match ip dst $WORKER2 flowid 1:10
docker exec $CONTAINER tc filter add dev $DEV protocol ip parent 1:0 prio 1 u32 \
   match ip dst $WORKER3 flowid 1:11

# second group

docker exec $CONTAINER tc qdisc add dev $DEV parent 1:10 handle 10: htb default 12
docker exec $CONTAINER tc class add dev $DEV parent 10: classid 10:1 htb rate 9999kbps ceil 9999kbps

docker exec $CONTAINER tc class add dev $DEV parent 10:1 classid 10:10 htb rate 3000kbps ceil 2000kbps
docker exec $CONTAINER tc class add dev $DEV parent 10:1 classid 10:11 htb rate 4000kbps ceil 4000kbps
docker exec $CONTAINER tc class add dev $DEV parent 10:1 classid 10:12 htb rate 9999kbps ceil 9999kbps

docker exec $CONTAINER tc filter add dev $DEV protocol ip parent 10:0 prio 1 u32 \
   match ip dst $WORKER1 flowid 10:10
docker exec $CONTAINER tc filter add dev $DEV protocol ip parent 10:0 prio 1 u32 \
   match ip dst $WORKER2 flowid 10:11
