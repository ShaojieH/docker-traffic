DEV="${1}"

tc qdisc del dev $DEV root
tc qdisc add dev $DEV parent root handle 1:0 htb default 22
tc class add dev $DEV parent 1:1 classid 1:22 htb rate 8000kbps ceil 8000kbps
tc class add dev $DEV parent 1:0 classid 1:1 htb rate 9999kbps ceil 9999kbps
tc class add dev $DEV parent 1:1 classid 1:10 htb rate 6000kbps ceil 6000kbps
tc filter add dev $DEV protocol ip parent 1:0 prio 1 u32 match ip dst 172.18.0.4 \
 flowid 1:10
tc filter add dev $DEV protocol ip parent 1:0 prio 1 u32 match ip dst 172.18.0.3 \
 flowid 1:10
tc filter add dev $DEV protocol ip parent 1:0 prio 1 u32 match ip dst 172.18.0.6 \
 flowid 1:10
tc class add dev $DEV parent 1:1 classid 1:11 htb rate 1000kbps ceil 1000kbps
tc filter add dev $DEV protocol ip parent 1:0 prio 1 u32 match ip dst 172.18.0.5 \
 flowid 1:11
tc qdisc add dev $DEV parent 1:10 handle 10:0 htb default 22
tc class add dev $DEV parent 10:1 classid 10:22 htb rate 8000kbps ceil 8000kbps
tc class add dev $DEV parent 10:0 classid 10:1 htb rate 9999kbps ceil 9999kbps
tc class add dev $DEV parent 10:1 classid 10:10 htb rate 2000kbps ceil 2000kbps
tc filter add dev $DEV protocol ip parent 10:0 prio 1 u32 match ip dst 172.18.0.4 \
 flowid 10:10
tc class add dev $DEV parent 10:1 classid 10:11 htb rate 4000kbps ceil 4000kbps
tc filter add dev $DEV protocol ip parent 10:0 prio 1 u32 match ip dst 172.18.0.3 \
 flowid 10:11
tc filter add dev $DEV protocol ip parent 10:0 prio 1 u32 match ip dst 172.18.0.6 \
 flowid 10:11
tc qdisc add dev $DEV parent 10:11 handle 100:0 htb default 22
tc class add dev $DEV parent 100:1 classid 100:22 htb rate 8000kbps ceil 8000kbps
tc class add dev $DEV parent 100:0 classid 100:1 htb rate 9999kbps ceil 9999kbps
tc class add dev $DEV parent 100:1 classid 100:10 htb rate 4000kbps ceil 4000kbps
tc filter add dev $DEV protocol ip parent 100:0 prio 1 u32 match ip dst 172.18.0.3 \
 flowid 100:10
tc class add dev $DEV parent 100:1 classid 100:11 htb rate 3000kbps ceil 3000kbps
tc filter add dev $DEV protocol ip parent 100:0 prio 1 u32 match ip dst 172.18.0.6 \
 flowid 100:11