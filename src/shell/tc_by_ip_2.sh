#!/bin/bash
set -x

INTERFACE="${1}"
SRC="${2}"
LIMIT="${3}"

tc qdisc del dev $INTERFACE root
tc qdisc add dev $INTERFACE root handle 1: cbq avpkt $LIMIT bandwidth 100mbit

# setup a class to limit to LIMIT kiloBytes/s
tc class add dev $INTERFACE parent 1: classid 1:1 cbq rate "$LIMIT"kBit \
   allot $LIMIT prio 5 bounded isolated
# add traffic from SRC to that class
tc filter add dev $INTERFACE parent 1: protocol ip prio 16 u32 \
   match ip src $SRC flowid 1:1