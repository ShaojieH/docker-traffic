#!/bin/bash
set -x

INTERFACE=veth09daa3c # /docker-spark_worker_3
DST=172.18.0.2
LIMIT=500

tc qdisc del dev $INTERFACE root
tc qdisc add dev $INTERFACE root handle 1: cbq avpkt 1000 bandwidth 100mbit

# setup a class to limit to LIMIT kiloBytes/s
tc class add dev $INTERFACE parent 1: classid 1:1 cbq rate "$LIMIT"kBit \
   allot $LIMIT prio 5 bounded isolated
# add traffic to DST to that class
tc filter add dev $INTERFACE parent 1: protocol ip prio 16 u32 \
   match ip dst $DST flowid 1:1