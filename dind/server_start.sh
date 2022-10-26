#!/bin/bash

sysctl -p
mount -t debugfs none /sys/kernel/debug
dockerd -H unix:///var/run/docker.sock -H tcp://0.0.0.0:2375 &
cd CHIMAclient

while ! ifconfig | grep -o -E ".+?-eth0"
do
    sleep 5
done

python3 main.py -i $(ifconfig | grep -o -E ".+?-eth0") &

while ! DOCKER_HOST=localhost:2375 docker load < /python_alpine.tar;
do
    sleep 5
done
