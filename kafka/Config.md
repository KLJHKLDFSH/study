# Configs

### Topic-Level Configs

- create topic

```sh
./bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic my-topic --partitions 1 --replication-factor 1 --config max.message.bytes=64000 --config flush.messages=1
```

- update topic

```sh
./bin/kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name my-topic --alter --add-config max.message.bytes=128000
```



|    sd  |      |      |
| ---- | ---- | ---- |
|      |      |      |
|      |      |      |
|      |      |      |

