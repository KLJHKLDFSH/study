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

A criticak aspect in stream processing is the notion of time, and how it is modeled and integrated. For example, some operations such as windowing are defined based on time boundaries.

流处理的一个关键方面是时间的概念，以及如何建模和集成它。例如，windowing 是基于时间边界定义的。



common notions of time in streams are:

- **Event time:** The point in time when an event or data record occurred, i.e. was originally created "at the source". Example: if the event is geo-localtion change reported by a GPS sensor in a car, then the associated event-time would be the time when the GSP sensor captured the localtion change.

  ```
  事件时间： 事件或数据记录发生的时间点，例子：如果事件是汽车中的GPS传感器报告的地理位置变化，那么相关的事件时间就是GPS传感器捕获到位置变化的时间。
  ```

- **Processing time:** The point in time when the event or data record happend to be processed by the streams processing appliction, i.e. when the record is being consumed. The processing time may be milliseconds, hours, or days etc. later than the orginal event time. **Example:** Imagine an analytics application that reads and processes the geo-localtion data reported from car sensors to present it to a fleet management dashboard.Here, processing-time in the analytics application might be  milliseconds or seconds(e.g for real-time piplines based on Apache Kafka and Kafka Streams) or hours(e.g. for batch pipelines based on Apache Hadoop or Apache Spark) after event-time.

  ```
  处理时间： 事件或记录发生在被流处理应用处理时的时间点，例如当记录被消费时。处理时间或许是毫秒，秒，小时，天。但晚于原始的事件时间。例子：想象一下分析程序在读和处理从车载传感器提交的地理数据并展示在车队管理仪表盘。这里，处理时间是在事件时间之后几豪秒、几秒、几小时。（取决与处理程序）
  ```

- **Ingestion time:** The point in time when an event or data record is stored in a topic partition by Kafka broker.The difference to event time is that this ingestion timestamp is generated when the record is appended to the target topic by the Kafaka broker, not when the record is create "at the source". The difference to procesessing time is that processing time is when the stream processing application processes the record. **For example**, if a record is never processed, there is no notion of processing time for it, but it still has an ingestion time.

  ```
  摄取时间：事件或数据记录通过Kafka broker 存储到topic 分区的时间点。不同与事件时间的是摄取时间戳是当记录被添加到指定的topic 分区时通过Kafka broker生成的，而不是“源头”创建记录时生成的。它与处理时间的区别在于处理时间是流处理应用处理记录的时间。例子：如果记录从未被处理过，它没有处理时间的概念，但是它一直有摄取时间。
  ```

The choice between event-time and ingestion time is actually done through the configuration of Kafka(not Kafka Streams): From Kafka 0.10.x onwards, timestamps are automatically embedded into Kafka messages. Depending on Kafka's configuration these timestamps represent event-time or ingestion-time. The respective Kafka configuration setting can be specified on the broker level or per topic.The default timestamp extractor in Kafka Streams will retrieve these embedded timestamps as-is. Hence, the effective time sematics of your application depend on the effiective kafka configuration for these embedded timestamps.

```
事件时间和摄入时间之间的选择实际上是通过Kafka的配置来完成的。（而不是kafka Streams）:自从kafka 0.10.x 开始，时间戳自动嵌入到kafka 消息中。根据kafka的配置，这些时间戳表示时间时间或者摄入时间。可以在代理级别或每个主题上指定相应的kafka配置设置。Kafka Streams 中的默认时间戳提取器将按原样提取这些嵌入的时间戳。因此，你应用程序的有效的时间语义取决于这些嵌入式时间戳的有效kafka配置。
```



Kafka Streams assigns a **timestamp** to every data record via the `TimestampExtractor` interface. These per-record timestamps describe  the progress os a stream with regards to time and are leveraged by time-dependent operations such as window operations.As a result, this time will only advance when a new record arrives at the processor. We call this data-driven time the **stream time** of the application to differentiate will the wall-clock time when this application is actually executing.Implementations of the `TimestampExtractor` interface willthen provide different semantics to the stream time definition. For example retrieving or computing timestamps based on the actual contents of data records such as an embedded timestamp field to provide event time semantics, and returning the current wall-clock time thereby yield processing time semantics to stream time. Developers can thus enforce different notions of time depending on their business needs.

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

- When new output records are generated via periodic funcations such as `Punctuator#punctuate()`,  the output record timestamp is defined as the current internal time (obtianed through context.timestamp() ) of the stream task.

  ```
  通过周期性函数(例如 Punctuator#punctuate())生成新的输出记录时，输出记录时间戳定义为流任务的当前内部时间（通过context.timestamp()获得）。
  ```

  

- For aggregations, the timestamp of a result update record will be the maximum timestamp of all input records contributing to the result.

  ```
  对于聚合，结果更新记录的时间戳将是对结果有贡献的所有输入记录的最大时间戳。
  ```

  

You can change the default behavior in the Processor Api by assigning timestamps to output records explicitly when calling `#forword()`.

```
你可以通过在调用forword()时显示地将时间戳分配给输出记录来更改Processor Api中的默认行为。
```

For aggregations and joins, timestamp are computers by using the follwing rules:

- For joins `stream-steam`, `table-table` that have left and right input records, the timestamp of the output record timestamp is assigned `max(left.ts, right.ts)`.

  ```
  对于具有左右输入记录的联接，输出记录时间戳分配为max(left.ts, right.th)
  ```

- For `stream-table` joins, the output record is assigned the timestamp from the stream record.

  ```
  对于流和表的联接，输出记录的分配来源流记录
  ```

- For aggregations, Kafka Streams also computes the max timestamp over all recoreds, per key, either globally(for non-windowed) or per-window.

  ```
  对于聚合，kafka stream 还可以全局或针对每一个窗口，针对每个键计算所有记录的最大时间戳。
  ```

- For stateless operations, the input recored timestamp is passed through. For `flatMap` and siblings that emit multiple records, all output records inherit the timestamp from the corresponding input record.

  ```
  对于无状态操作，将传递输入记录时间戳。对于发出多个记录的flatMap和同级，所有输出记录都从相应的输入记录继承时间戳。
  ```

  

### Duality Of Streams and Tables



### Aggregations



### Windowing



### States



## Processing Guarantees



### Out-of-Order handling45
