### Quick Start

https://kafka.apache.org/quickstart

1. ###### 运行zookeeper 

   ```shell
   sudo sh bin/zookeeper-server-start.sh config/zookeeper.properties
   ```

2. ###### 运行kafka

   ```sh
   sudo sh bin/kafka-server-start.sh config/server.properties
   ```

####  使用

-  创建Topic

```shell
sudo sh bin/kafka-topics.sh --create  --bootstrap-server localhost:9092 --topic quickstart-events
sudo sh bin/kafka-topics.sh --create  --bootstrap-server localhost:9092 --topic quickstart-events --partitions 5
sudo sh bin/kafka-topics.sh --create  --bootstrap-server localhost:9092 --topic quickstart-events --partitions 8 --replication-factor 2 
```

- 查看topic

```shell
sudo sh bin/kafka-topics.sh --describe  --bootstrap-server localhost:9092 --topic quickstart-events
```

- 写入事件

```shell
sudo sh bin/kafka-console-producer.sh --property parse.key=true --bootstrap-server localhost:9092 --topic quickstart-events
```

- 读取事件

```shell
sudo sh bin/kafka-console-consumer.sh --from-beginning --bootstrap-server localhost:9092 --topic quickstart-events 
```

- 删除Topic

```sh
sudo bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic quickstart-events
```

-  查看全部topic

```SH
sudo bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

