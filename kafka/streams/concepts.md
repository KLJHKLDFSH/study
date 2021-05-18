# Stream Concepts



### Some highlights of Kafka Streams:

- Designed as a **simple and lightweight client library**, which can be easily embedded in any Java application and integrated with any existing packaging, deployment and operational tools that users have for their streaming applications.

  ```
  设计为简单和轻量级的客户端库
  ```

- Has **no external dependencies on systems other than Apache Kafka itself** as the internal messaging layer; notably, it uses Kafka's partitioning model to horizontally scale processing while maintaining strong ordering guarantees.

  ```
  除了Kafka内部的消息传递层外，没有任何外部依赖。
  ```

- Supports **fault-tolerant local state**, which enables very fast and efficient stateful operations like windowed joins and aggregations.

  ```
  支持容错本地状态，这可以实现非常快速和高效的有状态操作，例如窗口连接和聚合。
  ```

- Supports **exactly-once** processing semantics to guarantee that each record will be processed once and only once even when there is a failure on either Streams clients or Kafka brokers in the middle of processing.

  ```
  支持一次精确的处理意义，以确保即使在流客户端或者kafka brokers在处理中出现错误时，每个记录也只会被处理一次。
  ```

- Employs **one-record-at-a-time processing** to achieve millisecond processing latency, and supports **event-time based windowing operations** with out-of-order arrival of records.

  ```
  采用一次一个记录的处理以实现毫秒级处理延迟，并支持以事件时间为基础的窗口操作以及记录的无序到达。
  ```

- Offers necessary stream processing primitives, along with a **high-level Streams DSL** and a **low-level Processor API**.

  ```
  提供必要的流处理原语，以及高级的 StreamsDSL 和 低级的 Processor Api
  ```



### Stream processing Topology（流处理拓扑）

- A stream is the most important abstraction provided by Kafka Streams: it represents an un bounded, continuously updating data set. A stream is an ordered, replayable, and fault-tolerant sequence of immutable data records, where a data record is defined as a key-value pair.

  ```
  流是kafka Streams 提供的一个重要的概念：它是一个无限的、不停更新的数据集，它是有序的、可重播和容错序列，其中数据记录被定义为键值对;
  ```

- A stream processing application is any program that makes use of Kafka Streams library. it defines its computational logic through one or more processor topologies, where a processor topology is graph of   stream processors(nodes) that are connected by streams(edges).

  ```
  流处理应用是使用Kafka Streams库的任何程序。他通过一个或多个处理器拓扑定义计算逻辑，其中处理器拓扑是由流(边)连接的流处理器（节点）的图.
  ```

- A stream processor is a node in the processor topology; it represents a processing step to transform data in streams by receiving one input record at a time from **its** upstream processors in the topology, applying its operation to it, and may subsequently produce one or more output records to its downstream processors.

  ```
  流处理器是一个处理器拓扑中的一个节点，它代表通过上游处理器接受一条输入记录来转换流中数据的处理步骤，对其应用操作，然后可能生产一个或多个输出记录到下游处理器。
  ```

#### there are two special processors in the topology:

- **Source Processor**: A source processor is special type of stream processor that does not have any upstream processors. it produces an input stream to its topology from one or more multiple Kafka topics by consuming records from there topics and forwarding them to its down-streams processors.

  ```
  源处理器： 源处理器是一个特殊流处理器类型，它没有上游处理器。它通过使用一个或多个Kafka 主题中的记录，并将它们转发到其下游处理器，从而从一个或多个Kafka 主题中生成拓扑结构的输入流
  ```

- **Sink Processor:** A sink processor is special type of stream processor that does not have and downstream processors. it sends any received records from its up-stream processors to a specified Kafka topic.

  ```
  sink 处理器一个特殊的流处理器类型，它没有下游处理器。它将所有从上游处理器中接受到的记录发送到指定地topic中。
  ```

  ![img](https://kafka.apache.org/28/images/streams-architecture-topology.jpg)



Kafka Streams offers two ways to define the stream processing topology;

- **Kafka Streams DSL** provides the most common data transformation operations such as `map`, `filter`, `join` and `aggregations` out of the box; 
- Processor API: lower-level, allows developers define and connect custom processors as well as to interact with state stores.

```
 低级的API 在处理状态存储时有更大的灵活性。不过，在DSL 中也可以嵌入低级API。
```

A processor topology is merely a logical abstraction for your stream processing code. At runtime, the logical topology is instantiated and replicated inside the application for parallel processing

```
处理器拓扑仅仅是流处理代码上的逻辑抽象。在运行时，逻辑拓扑是被实例化并被复制到应用程序内部进行并行处理的。（会在结构篇中详细讲述）
```



![img](https://kafka.apache.org/28/images/streams-architecture-overview.jpg)

### Time

A critical aspect in stream processing is the notion of time, and how it is modeled and integrated. For example, some operations such as windowing are defined based on time boundaries.

流处理的一个关键方面是时间的概念，以及如何建模和集成它。例如，windowing 是基于时间边界定义的。



common notions of time in streams are:

- **Event time:** The point in time when an event or data record occurred, i.e. was originally created "at the source". Example: if the event is geo-location change reported by a GPS sensor in a car, then the associated event-time would be the time when the GSP sensor captured the location change.

  ```
  事件时间： 事件或数据记录发生的时间点，例子：如果事件是汽车中的GPS传感器报告的地理位置变化，那么相关的事件时间就是GPS传感器捕获到位置变化的时间。
  ```

- **Processing time:** The point in time when the event or data record happens to be processed by the streams processing application, i.e. when the record is being consumed. The processing time may be milliseconds, hours, or days etc. later than the original event time. **Example:** Imagine an analytics application that reads and processes the geo-location data reported from car sensors to present it to a fleet management dashboard. Here, processing-time in the analytics application might be  milliseconds or seconds(e.g for real-time pipelines based on Apache Kafka and Kafka Streams) or hours(e.g. for batch pipelines based on Apache Hadoop or Apache Spark) after event-time.

  ```
  处理时间： 事件或记录发生在被流处理应用处理时的时间点，例如当记录被消费时。处理时间或许是毫秒，秒，小时，天。但晚于原始的事件时间。例子：想象一下分析程序在读和处理从车载传感器提交的地理数据并展示在车队管理仪表盘。这里，处理时间是在事件时间之后几豪秒、几秒、几小时。（取决与处理程序）
  ```

- **Ingestion time:** The point in time when an event or data record is stored in a topic partition by Kafka broker. The difference to event time is that this ingestion timestamp is generated when the record is appended to the target topic by the Kafka broker, not when the record is create "at the source". The difference to processing time is that processing time is when the stream processing application processes the record. **For example**, if a record is never processed, there is no notion of processing time for it, but it still has an ingestion time.

  ```
  摄取时间：事件或数据记录通过Kafka broker 存储到topic 分区的时间点。不同与事件时间的是摄取时间戳是当记录被添加到指定的topic 分区时通过Kafka broker生成的，而不是“源头”创建记录时生成的。它与处理时间的区别在于处理时间是流处理应用处理记录的时间。例子：如果记录从未被处理过，它没有处理时间的概念，但是它一直有摄取时间。
  ```

The choice between event-time and ingestion time is actually done through the configuration of Kafka(not Kafka Streams): From Kafka 0.10.x onwards, timestamps are automatically embedded into Kafka messages. Depending on Kafka's configuration these timestamps represent event-time or ingestion-time. The respective Kafka configuration setting can be specified on the broker level or per topic. The default timestamp extractor in Kafka Streams will retrieve these embedded timestamps as-is. Hence, the effective time semantics of your application depend on the effective Kafka configuration for these embedded timestamps. 

```
事件时间和摄入时间之间的选择实际上是通过Kafka的配置来完成的。（而不是kafka Streams）:自从kafka 0.10.x 开始，时间戳自动嵌入到kafka 消息中。根据kafka的配置，这些时间戳表示时间时间或者摄入时间。可以在代理级别或每个主题上指定相应的kafka配置设置。Kafka Streams 中的默认时间戳提取器将按原样提取这些嵌入的时间戳。因此，你应用程序的有效的时间语义取决于这些嵌入式时间戳的有效kafka配置。
```



Kafka Streams assigns a **timestamp** to every data record via the `TimestampExtractor` interface. These per-record timestamps describe  the progress of  a stream with regards to time and are leveraged by time-dependent operations such as window operations. As a result, this time will only advance when a new record arrives at the processor. We call this data-driven time the **stream time** of the application to differentiate will the wall-clock time when this application is actually executing. Implementations of the `TimestampExtractor` interface will then provide different semantics to the stream time definition. For example retrieving or computing timestamps based on the actual contents of data records such as an embedded timestamp field to provide event time semantics, and returning the current wall-clock time thereby yield processing time semantics to stream time. Developers can thus enforce different notions of time depending on their business needs.

```
Kafka streams 通过 TimestampExtractor 接口分配一个时间戳到每一个数据记录。
```

```java
public interface TimestampExtractor{
    long extract(ConsumerRecord<java.lang.Object,java.lang.Object> record,long previousTimestamp)
}
```

Finally, whenever a Kafka Streams application writes records to Kafka, then it will also assign timestamps to these new records. The way the timestamps assigned depends on the context:

```
最后，每当kafka Streams 应用写记录到kafka时，它都会分配一个时间戳到这个新的记录中，分配时间戳的方法根据下面的情况来定：
```



- When new output records are generated via processing some input record, for example, `context.forward()` triggers in the `process()` function all, output record timestamps are inherited from input record timestamps directly.

  ```
  当处理一些数据记录生成新的输出记录时，例如，在process()函数调用中触发的 context.forward()，输出记录的时间戳是直接集成输入记录的时间戳的。
  ```

- When new output records are generated via periodic functions such as `Punctuator#punctuate()`,  the output record timestamp is defined as the current internal time (obtained through context.timestamp() ) of the stream task.

  ```
  通过周期性函数(例如 Punctuator#punctuate())生成新的输出记录时，输出记录时间戳定义为流任务的当前内部时间（通过context.timestamp()获得）。
  ```

  

- For aggregations, the timestamp of a result update record will be the maximum timestamp of all input records contributing to the result.

  ```
  对于聚合，结果更新记录的时间戳将是对结果有贡献的所有输入记录的最大时间戳。
  ```

  

You can change the default behavior in the Processor API by assigning timestamps to output records explicitly when calling `#forword()`.

```
你可以通过在调用forword()时显示地将时间戳分配给输出记录来更改Processor Api中的默认行为。
```

For aggregations and joins, timestamp are computers by using the following rules:

- For joins `stream-steam`, `table-table` that have left and right input records, the timestamp of the output record timestamp is assigned `max(left.ts, right.ts)`.

  ```
  对于具有左右输入记录的联接，输出记录时间戳分配为max(left.ts, right.th)
  ```

- For `stream-table` joins, the output record is assigned the timestamp from the stream record.

  ```
  对于流和表的联接，输出记录的分配来源流记录
  ```

- For aggregations, Kafka Streams also computes the max timestamp over all records, per key, either globally(for non-windowed) or per-window.

  ```
  对于聚合，kafka stream 还可以全局或针对每一个窗口，针对每个键计算所有记录的最大时间戳。
  ```

- For stateless operations, the input recored timestamp is passed through. For `flatMap` and siblings that emit multiple records, all output records inherit the timestamp from the corresponding input record.

  ```
  对于无状态操作，将传递输入记录时间戳。对于发出多个记录的flatMap和同级，所有输出记录都从相应的输入记录继承时间戳。
  ```

  

### Duality Of Streams and Tables

When implementing stream processing use cases in practice, you typically need both streams and also database. In other words, streams are everywhere , bu databases are everywhere too.

```
当在实际实施流处理案例中，你通常即需要流又需要数据库。
```

Any stream processing technology must therefore provide **first-class support for steams and tables.** Kafka's Streams API provides such functionality through its core abstractions for streams and tables, which we will talk about in a minute. Now , an interesting observation is that there is actually a close relationship between streams and tables, the so-called streams-table duality. And Kafka exploits this duality in many ways: for example , to make your applications elastic, to support fault-tolerant stateful processing, or to run interactive queries against you application's latest processing results. And beyond its internal usage, the Kafka Streams API also allows developers to exploit this duality in their own applications.

```
因此，任何流处理技术必须提供一流的流和表支持。Kafka Stream API 通过对流和表的核心抽象提供此类功能,我们将花一分钟来讨论它。一个有趣的观察是流和表之间其实有紧密的关系，所我我们称为流-表二元性。并且kafka在很多地方利用这种二元性。例如：让你的应用程序具有扩展性，支持容错状态处理，或者针对应用程序的最新处理结果运行交互式查询。而且处理内部使用外，Kafka streams api 也允许开发者在自己的应用程序中利用这种二元性。
```

Before we discuss concepts such as aggregations in Kafka Streams, we must first introduce tables in more detail, and talk about the aforementioned streams-tables duality. Essentially, this duality means that a stream can be viewed as a table, and a table can be viewed as stream. Kafka's log compaction feature, for example, exploits this duality.

```
在我们讨论如Kafka streams 中的聚合之类的概念之前，我们必须先更详细的介绍表。并且讨论之前的流-表二元性。本质上，这个二元性的意思是流可以看作是表，表格同样可以看作是流。kafka 的日志压缩特效就是利用了这个二元性。
```

A simple form of a table is a collection of key-value pairs, also called a map or associative array. Such a table may look as follows:

```
表的简单形式是键值对的集合，也叫映射或关联数组。这样的表可能如下：
```



![img](https://kafka.apache.org/28/images/streams-table-duality-01.png)

The stream-table duality describes the close relationship between streams and tables.

- **Stream as Table:** A stream can be considered a changelog of a table, where       each data record in the stream captures a state change of the table. A stream is thus a table in disguise, and it can be easily turned into a "real" table by replaying the changelog from beginning to end to reconstruct the table. Similarly, in a more general analogy, aggregating data records in a stream such as computing the total number of page views by user from a stream of pageview events will return a table(here with the key and the value being the user and its corresponding pageview count, respectively).

  ```
  流可以看作是表的日记变更，其中流中的每个数据都捕获表的状态变更。因此，流是变相的表。并且可以通过从头到尾重播变更日志以重新构建变，轻松的变成“真实”表。
  ```

- **Table as Stream:** A table can be considered a snapshot, at a point in time, of the latest value for each key in a stream(a stream's data records are key-value pairs). A table is thus a stream in disguise, and it can be easily turned into a "real" stream by iterating over each key-value entry in the table.

  ```
  可以将表看作某个时间点上流中的每个键的最新值的快照。因此，表是变相的流，并且它可以通过遍历表中的每个键值对轻松的转换为”真正“的流。
  
  转换为流：但不是表示转换为原来的流，流的数据发生的变更。
  ```



Let's illustrate this with an example. Imagine a table that tracks the total number of pageviews by user (first column of diagram below). Over time, whenever a new pageview event is processed, the state of the table is update accordingly. Here the state changes between different points in time - and different revisions of the table -can be represented as a changelog stream(second column).

```
让我们用一个例子来说明这一点。想象一下一张表，它用来追踪用户的总浏览量。随着时间的推移，新的浏览被处理，因此，这张表的状态一直在更新。在这里，状态在不同时间点的变化，表的不同版本可以表示为更改变更日志流（第二列）
```

![img](http://kafka.apache.org/28/images/streams-table-duality-02.png)

Interestingly, because of the stream-table duality, the same streams can be used to reconstruct the original table(third column).

```
有趣的是，由于流-表二元性，相同的流可以被用来重构原来的表。
```



![img](http://kafka.apache.org/28/images/streams-table-duality-03.png)

The same mechanism is used, for example, to replicate databases via change data capture(CDC) and, within Kafka Streams, to replicate its so-called state stores across machines for fault-tolerance. The stream-table duality is such an important concept that Kafka Streams models it explicitly via the `KStream`, `KTable`, and `GlobleTable` interface.

```
例如，使用相同的机制通过更改数据捕获复制数据库，并在Kafka Streams 中使用这种机制跨机器复制其所谓的状态存储以实现容错，流-表的二元性是一个非常重要的概念，Kafka Streams 通过KStream，Ktable，GlobleTable接口对其进行显式建模。
```



### Aggregations

An aggregation operation takes one input stream or table, and yields a new table by combining multiple input records into a single output record. Examples of aggregations are computing counts or sum.

```
聚合操作采用一个输入流或表，并通过合并多个输入记录为单个输出记录来生成一个新表。聚合的事例是计算计数和总和。
```

In the `Kafka Stream DSL`, an intput stream of an `aggregation` can be a KStream or a KTable, but the output stream will always be a Stable. This allows Kafka Streams to update an aggregate value upon the out-of-order arrival of further records after the value was produced and emitted. When such out-of-order arrival happens, the aggregations Kstream or KTable emits a new aggregate value. Because the output is a KTable, the new value is considered to overwrite the old value with the same key in subsequent processing steps.

```
在DSL中，聚合的输入流可以是KStream或KTable，但输出流始终是KTable。这使得Kafka Streams 在产生和发生值后，如果其他记录无序到达，则可以更新汇总值。当发生这种无序到达时，聚合的KStream或KTable会发出新的聚合值。由于输出是表，因此在后续的处理步骤中，新值将被视为使用相同的键覆盖旧值。
```

### Windowing

​	Windowing lets you control how to group records that have the same key for stateful operations such as `aggerattions` or `joins` into so-called windows. Windows are tracked per record key.

```
通过窗口，你可以控制如何对具有相同键的记录进行分组，以进行有状态操作（例如 聚合或加入所谓的窗口）。每个键都会跟踪windwos。
```

​	`Windows operations` are available in the `Kafka Stream DSL`. When working with windows, you can specify a grace period for the window. This grace period controls how long Kafka Streams will wait for out-of-order data records for a given window. if a record arrival after the grace period of a window has passed, the record is discarded and will not be processed in that window. Specifically, a record is discarded if its timestamp dictates it belongs to a window, but the current stream time is greater than the end of the window plus the grace period.

```
窗口操作在Kafka Stream DSL 中是可用的。当窗口运行时，你可以给窗口指定一个`#grace()` 期限。这个期限控制着Kafka Stream 将等待给定窗口多长时间的无序数据记录。如果一个记录在窗口期限过期后到达，那么这个记录被丢弃掉并且将不会在这个窗口中被处理。具体来说， 如果一条记录的时间戳指示它属于某个窗口，则该记录将被丢弃，但是当前流时间大于该窗口的末尾加上期限。
```

​	Out-of-order records are always possible  in the real world and should be properly accounted in you applications. It depends on the effective `time semantics` how out-of-order records are handled. in the processing-time, the semantics are "when the record is being processed". which means that the notion of out-of-order records is not applicable as, by definition, no record can be out-of-order. Hence, out-of-order records can only be considered as such for event-time. int both case, Kafka Streams is able to properly handle out-of-order records.

```
无序记录在现实世界总是会出现，应该在你的应用程序中适当的考虑。无须记录的处理根据准确的时间语义。处理时间的语义是：“当记录开始被处理时”，意味着无序记录的概念是不成立的，根据定义，没有记录可以是无序的。因此，无序记录只能被看作是事件时间，在这两种情况下，Kafka Streams 都能正确的处理无序记录。
```



### States

Some stream processing application don't require state, which means the processing of a message is independent from the processing of all other messages. However, being able to maintain state opens up many possibilities for sophisticated stream processing applications: you can join input streams, or group and aggregate data records. Many such stateful operators are provided by the Kafka Stream DSL.

```
一些流处理应用不需要状态，意味着消息处理是不依赖于来自任何其他消息的。然而，能够维持状态为复杂的流处理程序打开了许多可能性：你可以加入输入流，或者进行分组和聚合数据记录，Kafka Stream DSL 提供了许多这样有状态的操作。
```







## Processing Guarantees



### Out-of-Order handling45

