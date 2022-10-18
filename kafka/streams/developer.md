

# Using Kafka Streams

-To catch any unexpected exceptions, you can set an `java.lang.Thread.UncaughtExceptionHandler`

```java
streams.setUncaughtExceptionHandler((Thread thread, Throwable throwable) -> {
  // here you should examine the throwable/exception and perform an appropriate action!
});

```



# Processor Api

The Processor API can be used to implement both **stateless** as well as **stateful** operations, where the latter is achieved through the use of [state stores](http://kafka.apache.org/28/documentation/streams/developer-guide/processor-api#streams-developer-guide-state-store).



### Defining a stream processor



You can define a customized stream processor by implementing the `Processor` interface, which provides the `process()` API method. The `process()` method is called on each of the received records.



#### init

初始化方法，在Streams  构建任务阶段被调用。



#### process



#### close



#### forword

当使用`forword()` 发送给下行流时，消息会被分配一个时间绰，但是会有三种情况发生：

1. 如果`forword()` 在`process()`中被调用，输出的消息继承的是输入消息的时间戳。
2. 如果`forword()` 在`Punctuator.punctuate()`中被调用，输出的消息将继承punctuate 时间（stream time or system wall-clock time）

3. `forword()` 自身也允许修改时间戳。





#### schedule

###### 作用：

​	

###### 概念：

###### 用法

**Punctuator**

**PunctuationType**

- STREAM_TIME
- WALL_CLOCK_TIME





### State Stores

#### Defining and create a state store

​	可以通过实现 StateStore 接口开发自定义的状态存储器。

​	可以直接使用`StoreBuilder` 创建state store。



#### Fault-tolerant State Store

​	state store can be continuously backed up to a Kafka topic behind the scenes.

​	this topic is sometims referred to  as the state store's associated **<u>*changelog topic*</u>**, or its changelog. 

​	you can enable or disable the backup feature for a state store.

Fault-tolerant state stores are backed by a [compacted](https://kafka.apache.org/documentation.html#compaction) changelog topic. The purpose of compacting this topic is to prevent the topic from growing indefinitely, to reduce the storage consumed in the associated Kafka cluster, and to minimize recovery time if a state store needs to be restored from its changelog topic.

```
状态的存储的备份是通过changelog topic压缩的，压缩topic的目的是为了避免topic无限增长。
```



Fault-tolerant windowed state stores are backed by a topic that uses both compaction and deletion

```
容错窗口的状态存储是通过压缩和删除一个topic备份的。
```

