#!/usr/bin/env bash

set -e

python /root/wait_for_tcp.py zookeeper 2181 60

cd /root/kafka_2.12-1.1.1/

MIGRATED_001_FILE=/root/MIGRATED_001.txt

if [ ! -f $MIGRATED_001_FILE ]; then
    sed -i "s/localhost/zookeeper/" config/server.properties
    echo -e "\nlisteners=PLAINTEXT://$KAFKA_HOST:9092" >> config/server.properties
    sed -i "s/broker.id=0/broker.id=$BROKER_ID/" config/server.properties
    touch $MIGRATED_001_FILE
fi

bin/kafka-server-start.sh config/server.properties
