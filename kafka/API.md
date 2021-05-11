# API 的使用

### Kafka的API：

- Producer Api

- Consumer Api
- Kafka Streams Api
- Kafka Connect Api
- Admin Api



### KafkaStreams API

KafkaStreans API 是一个客户端库，用于应用程序和微服务。并且允许他们输入、输出数据并存储在Kafka集群中。



### Producer API

Producer API允许应用程序发送数据流到Kafka集群中的topics

要使用producer API需要引入依赖

```xml
<dependency>
  <groupId>org.apache.kafka</groupId>
  <artifactId``>kafka-clients</artifactId>
</dependency>
```



