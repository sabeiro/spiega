---
title: "Messaging"
author: Giovanni Marelli
date: 2019-07-02
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# Messaging 

Messaging distinguish between producers and consumers and arranges the messages into topics. To consume a topic the offset is used as a bookmark to efficiently navigate through the topic, consume only new messages or a particular subset.

## middleware 

Here is a [middleware in python](https://github.com/sabeiro/sawmill/blob/master/live_py/) to publish and consume messages from a topic. 

Endpoints are:

* `/push/<topic>` produce a message to a topic
* `/consume/<topic>` consume the whole topic
* `/latest/<topic>` returns the messages in the topic not already consumed
* `/latest_time/<topic>` returns the messages starting from a given time
* `/realtime/<topic>` shows the kafka stream
* `/delete/<topic>` deletes a topic
* `/topics/` shows the topics
* `/spec` swagger documentation
* `/` app user interface

## Kafka

Kafka is deployed using a [docker-compose](https://github.com/sabeiro/sawmill/blob/master/docker/kafka/docker-compose.yml) file.

This includes **zookeper** which contains the volumes for storing the topic contents.

```
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    hostname: zookeeper
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    volumes:
      - zk-data:/var/lib/zookeeper/data # for Data
      - zk-txn-logs:/var/lib/zookeeper/log # for transaction logs
 
```
**kafka** engine which requires a careful definition of the listeners

```
  kafka:
    image: confluentinc/cp-kafka:latest
    hostname: kafka
    container_name: kafka
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,OUTSIDE:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: INTERNAL://kafka:9093,OUTSIDE://host.docker.internal:9092
      KAFKA_LISTENERS: INTERNAL://:9093,OUTSIDE://:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_RETENTION_MS: 604800000
      KAFKA_RETENTION_BYTES: -1
    extra_hosts:
      - "host.docker.internal:172.0.0.1"
```
and eventually an **UI**

```
  kafka-ui:
    #image: confluentinc/cp-enterprise-control-center:latest
    image: docker.redpanda.com/vectorized/console:latest
    #hostname: control-center
    depends_on:
      - kafka
    # ports:
    #   # - "9021:9021"
    #   - "127.0.0.1:9021:8080"
    environment:
      KAFKA_BROKERS: 'kafka:9093'
      PORT: 9021
```

## mosquitto

Mosquitto is designed for IoT where many devices are sending information (in a log fashion) to a central server. User applications can then consume topics and run analytics.

## kinesis


## pubsub
