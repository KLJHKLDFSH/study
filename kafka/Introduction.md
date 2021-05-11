### Introduction

三个特性

1. 可以让你发布和订阅流式的记录。这一方面与消息队列或者企业消息系统类似。 
2. 可以储存流式的记录，并且有较好的容错性。
3. 可以在流式记录产生时就进行处理。



主要的概念和术语

##### Event：

事件：可以是条信息或者记录。

在向Kafka读取或写入数据时，将以事件的形式形式进行操作。

事件包含的信息:

- key
- value
- timestamp
- optional metadata

例子：

- Event key: "KAFKA"
- Event Value：“消息中间件”
- Event timestamp：“2020-12-01 16:44”



##### Producers

##### Consumers

##### topic

​	Evenet 被组织和存储在topic中，topic就像是文件系统中的文件夹，而Event就是文件夹下面的文件，Event key就是文件的名称

​	partition : 在kafka中topic是被分区的。当第一次写入\读取时使用了哪一个分区，之后的写入\读取都在这个分区中进行

<img src="http://kafka.apache.org/images/streams-and-tables-p1_p4.png" alt="img" style="zoom:50%;" />

图：通过网络将事件写入主题分区，两个不同的客户端正在彼此独立的新发布事件。

​		具有相同键的事件被写入同一个分区。



### API 

- Admin API

  说明：用于管理和检查topics、brokers、和其他kafka 对象

- Producer Api

  说明：用于发布

- Consumer Api

- Kafka Streams Api

- Kafka Connect Api

- Admin Api

