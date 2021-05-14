### KStream

概念：

 	KSteam 是 消息流的 抽象，其中每一个数据都是无边界的数据集中独立的一份。

​	KStream 中没有更新的概念，所有的数据都是**新增**的。

​	



### KTable

概念：

​	KTable 是变更日志流的抽象。其中的每一个数据表示一次变更。

​	就是数据库的概念。

​	最后呈现出结果是多个变更的最终结果。



### **Global Table**

概念:

​	将topic的数据流写入GlobalTable，topic的数据将被解释为变更日志流

​	当数据不为null时，定义为insert / update ，如果数据为null，则定义为删除；



### Transfrorm a stream



### Stateless transformations

- Branch

  ​	KStream → KStream[]

     使用Predicates将一条流分为多条流。

- Filter

  - KStream → KStream

  - KTable → KTable

    过滤掉不满足条件的数据

- **Inverse Filter**

  - KStream → KStream

  - KTable → KTable

    Evaluates a boolean function for each element and drops those for which the function returns true. ([KStream details](http://kafka.apache.org/27/javadoc/org/apache/kafka/streams/kstream/KStream.html#filterNot-org.apache.kafka.streams.kstream.Predicate-), [KTable details](http://kafka.apache.org/27/javadoc/org/apache/kafka/streams/kstream/KTable.html#filterNot-org.apache.kafka.streams.kstream.Predicate-))

    ```
    KStream<String, Long> stream = ...;
    
    // An inverse filter that discards any negative numbers or zero
    // Java 8+ example, using lambda expressions
    KStream<String, Long> onlyPositives = stream.filterNot((key, value) -> value <= 0);
    
    // Java 7 example
    KStream<String, Long> onlyPositives = stream.filterNot(
        new Predicate<String, Long>() {
          @Override
          public boolean test(String key, Long value) {
            return value <= 0;
          }
        });
    ```

- **FlatMap** 
  - KStream → KStream

  偏平化映射，将一条数据映射为多条，且可以修改值



**GroupByKey**

- KStream → KGroupedStream

对键进行分区

分区是聚合流或表的先决条件。确保数据进行适当的分区以进行后续的操作。

分组与窗口化: 窗口操作是一个相关操作，它使您可以控制如何将同一个键的分组记录“分组”到所谓的窗口中，以进行有状态的操作，例如窗口聚合或窗口联接。





**SelectKey**

- KTable → KStream

为每一个数据分配一个新的key(将会导致从新分区)

```
KStream<byte[], String> stream = ...;

// Derive a new record key from the record's value.  Note how the key type changes, too.
// Java 8+ example, using lambda expressions
KStream<String, String> rekeyed = stream.selectKey((key, value) -> value.split(" ")[0])

```





**Table to Stream**

- KStream → KTable

获取这个表的变更日志记录（不是将表当前的数据转换为stream ，而是获取变更记录）

```
KTable<byte[], String> table = ...;

// Also, a variant of `toStream` exists that allows you
// to select a new key for the resulting stream.
KStream<byte[], String> stream = table.toStream();
```

**Stream to Table**

将流转为表，

```
KStream<byte[], String> stream = ...;

KTable<byte[], String> table = stream.toTable();
```

**Repartition**

重分区



Generated topic is treated as internal topic, as a result data will be purged automatically as any other internal repartition topic

生成的主题被视为内部主题，因此数据将像任何其他内部分区主题一样自动清除





```
KStream<byte[], String> stream = ... ;
KStream<byte[], String> repartitionedStream = stream.repartition(Repartitioned.numberOfPartitions(10));
```





### Stateful transformations



关系图

![img](http://kafka.apache.org/27/images/streams-stateful_operations.png)



时间窗口



| Window name                                                  | Behavior      | Short description                                            |
| :----------------------------------------------------------- | :------------ | :----------------------------------------------------------- |
| [Tumbling time window](https://kafka.apache.org/23/documentation/streams/developer-guide/dsl-api.html#windowing-tumbling) | Time-based    | Fixed-size, non-overlapping, gap-less windows                |
| [Hopping time window](https://kafka.apache.org/23/documentation/streams/developer-guide/dsl-api.html#windowing-hopping) | Time-based    | Fixed-size, overlapping windows                              |
| [Sliding time window](https://kafka.apache.org/23/documentation/streams/developer-guide/dsl-api.html#windowing-sliding) | Time-based    | Fixed-size, overlapping windows that work on differences between record timestamps |
| [Session window](https://kafka.apache.org/23/documentation/streams/developer-guide/dsl-api.html#windowing-session) | Session-based | Dynamically-sized, non-overlapping, data-driven windows      |

#### Tumbling time windows

翻滚时间窗也是基于时间间隔的，但它是固定大小、不重叠、无间隙的窗口。

![streams-time-windows-tumbling](https://kafka.apache.org/23/images/streams-time-windows-tumbling.png)

#### Hopping time window

跳跃时间窗口是基于时间间隔的，它有固定大小的重叠时间窗口

![img](http://kafka.apache.org/27/images/streams-time-windows-hopping.png)

#### Sliding time window

滑动窗口实际上与跳跃和翻滚窗口完全不同。在Kafka Streams中，滑动窗口仅用于联接操作，并且可以通过JoinWindows类指定。

![img](http://kafka.apache.org/27/images/streams-sliding-windows.png)

#### Session Window

Session window 用于将基于key的事件聚合为所谓的会话，其过程称为会话化。

会话代表一段活动时间，该活动时间由已定义的活动间隔（或“空闲”）隔开。

落入任何现有会话的不活动间隙内的所有已处理事件都将合并到现有会话中。

如果某个事件超出了会话间隔，则将创建一个新的会话。



![streams-session-windows-02](https://kafka.apache.org/23/images/streams-session-windows-02.png)

```

```

#### SessionWindowedKStream.aggregate

Params

- initializer - 一个初始化程序，用于计算初始中间聚合结果。 不能为null。

- aggregator - 计算新聚合结果的聚合器。 不能为null。

- sessionMerger - 合并两个聚合结果的合并。 不能为null。

  

通过分组的键和定义的会话聚合此流中记录的值。

请注意，会话是基于每个键生成的，具有不同键的记录会创建独立的会话。

具有空键或值的记录将被忽略。

聚合是通过reduce（...）进行合并的一种概括，因为它例如允许结果具有与输入值不同的类型。

结果被写入本地SessionStore（基本上是一个不断更新的实例化视图）。

此外，对存储的更新将向下游发送到KTable更新日志流中。
在处理每个会话的第一个输入记录之前，将直接应用指定的Initializer，以提供初始中间聚合结果，该结果用于处理每个会话的第一个记录。

指定的Aggregator将应用于每个输入记录，并使用当前聚合（或使用通过Initializer提供的中间聚合结果用于第一条记录）来计算新的聚合和记录的值。

指定的合并用于将两个现有会话合并为一个，即，当窗口重叠时，它们将合并为单个会话，而旧会话将被丢弃。

因此，aggregate（）可用于计算诸如count（c.f. count（））之类的聚合函数。
配置中的默认键和值serde将用于序列化结果。

如果需要其他serde，则应使用aggregate（Initializer，Aggregator，Merge，Materialized）。
并非所有更新都可以向下游发送，因为内部缓存用于将对同一窗口和键的连续更新重复数据删除。

传播更新的速率取决于您的输入数据速率，不同键的数量，并行运行的Kafka Streams实例的数量，以及高速缓存大小和提交时间间隔的配置参数。
对于故障和恢复，存储将由内部变更日志主题支持，该主题将在Kafka中创建。 changelog主题将命名为“ $ {applicationId}-$ {internalStoreName} -changelog”，其中“ applicationId”是用户在StreamsConfig中通过参数APPLICATION_ID_CONFIG指定的，“ internalStoreName”是内部名称，“-changelog”是固定的后缀。请注意，内部商店名称可能无法通过交互式查询来查询。
您可以通过Topology.describe（）检索所有生成的内部主题名称。







# 笔记

没有key 时，groupbykey() 会跳过该records