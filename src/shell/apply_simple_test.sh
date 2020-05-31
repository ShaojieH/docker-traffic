#!/bin/bash
set -x

CONTAINER="04909c27d057"
DST_IP="172.18.0.5"
LIMIT="2000"

docker exec $CONTAINER tc qdisc add dev eth0 root handle 1: htb default 12
# 在root下添加HTb qdisc，handle名称为1:
docker exec $CONTAINER tc class add dev eth0 parent 1: classid 1:1 htb rate "$LIMIT"kbps ceil "$LIMIT"kbps
# 在该qdisc下添加htb子类，设置最低和最高传输速率
docker exec $CONTAINER tc filter add dev eth0 parent 1: protocol ip prio 16 u32 match ip dst $DST_IP flowid 1:1
# 将IP地址符合172.18.0.5的包由1:分类至1：1
