# Architecture

Kafka Streams simplifies application development by building on the Kafka producer and consumer libraries and leveraing the native capabilities of Kafka to offer data parallelism, distributed coordination ,fault tolerance, and operational simplicity. In this section, we describe how Kafka Streams works underneath the covers.

The picture below shows the anatomy of an application that uses the Kafka Streams libriry. Let's walk through some details.

![img](http://kafka.apache.org/28/images/streams-architecture-overview.jpg)

## Stream partitions and Tasks

The message layer of Kafka partitions data for storing and transporting it. Kafka Streams partition data for processing it. In both cases, this partitions what enables data locality, elasticity, scalability, high performance, and fault tolerance. Kafka Streams uses the concepts of partitions and tasks as logical units of its parallelism model based on Kafka topic partitions. There are close links between Kafka Streams and Kafka in the context of parallelism:

```
Kafka的消息层对数据分区是为了存储和传输它，Kafka Streams 对数据分区是为了处理它。在这两种情况下，这种分区可以实现数据的局部性，弹性，可伸缩性，高性能，和容错能力。Kafka Streams使用分区和任务作为基于Kafka topic 分区的并发模型的逻辑单元。Kafka Streams 和 Kafka 在并发环境中两者的关联是：
```

- Each stream partition is a totally sequence of data records and maps to a Kafka topic partition.

  ```
  每一个流分区是数据记录的完全排序的序列，并映射到Kafka主题分区。
  ```

- A data record in the stream maps to a Kafka message from that topic.

  ```
  流中的数据记录映射到来自该主题的Kafka消息。
  ```

- The keys of data records determine the partitioning of data in both Kafka and Kafka Streams, i.e. how data is routed to specific partitions within topics.

  ```
  数据记录的key 决定着数据在Kafka和Kafka Streams中的分区。即数据是如何路由到指定的topic分区的。
  ```



An application's processor topology is scaled by breaking it into multiple tasks. More specifically, Kafka Streams creates a fixed number of tasks based on the input stream partitions for the application, with each task assigned a list of partitions from the input streams(i.e. Kafka topics). The assignment of partitions to tasks never changes so that each task is a fixed unit of parallelism of the application. Tasks can then intsantiate their own processor topology based on the assigned partitions; they also maintain a buffer for each of its assigned partitions and process message one-at-a-time from there record buffers. As a result stream tasks can be processed indecently and in parallel without manual intervention.

```
通过应用程序的处理器拓扑划分为多个任务来扩展它的规模。更详细地说：Kafka Streams 为应用程序创建基于输入流分区的固定数量的任务。并且为每个任务分配来自输入流的分区列表（即：Kafka topic）。分区分配到任务是不会改变的，所以每个任务都是应用程序并行性的固定单元。然后任务能基于分配的分区实例化他们自己的处理拓扑；它们也为每一个分配的分区维护一个Buffer，并一次处理来自这些记录缓冲区的消息。结果，可以在没有人工干预的情况下独立地并行处理流任务。
```

Slightly simplified, the maximum parallelism at which your application may run is bounded by the maximum number of stream tasks,  which itself is determined by maximum number of partitions of the input topic the application is read from. For example, if your input topic hash 5 partitions, then you run up to 5 applications instances. These instances will collaboratively process the topic's data, if you run a larger number of app instances than partitions of the input topic, the "excess" app instances will launch but remain idlel however, if one of the busy instances goes down, one of the idle instances will resume the former's work.

```
稍微简化一下，你应用程序可以运行的最大并行度受流任务的最大数量限制，而流任务本身则由应用程序正在读区的输入主题的最大分区数量决定。例如，如果您的输入主题有5个分区，那么你最多可以运行5个应用程序实例。这些实例将共同处理主题数据。如果运行的应用程序实例数量大于输入主题的分区数量，则“过多”的应用程序实例将启动，但保持空闲状态；但是，如果其中一个繁忙实例发生故障，则其中一个空闲实例将恢复前者的工作。
```

It is important to understand that Kafka Streams is not a resource manager, but a library that "runs" anywhere its stream processing application runs. Multiple instances of the application are executed either on the same machine, or spread across multiple machines and tasks can be distributed automatically by the library to those running application instances. The assignment of partitions to tasks never changes; If an application instance fails, all its assigned tasks will be automatically restarted on other instances and continue to consumer from the same stream partitions.

```
Kafka 不是一个资源管理器，而是一个可以在其流处理应用程序运行的任何地方运行的库。在同一台计算机上执行该应用程序的多个实例，也可以分布在多台计算机上，并且库可以自动将任务分配给那些正在运行的应用程序实例。分配分区给任务永远不会改变。如果一个应用程序实例失败，所有分配给它的任务将在其他实例上自动重启，并继续从相同的流分区消费。
```

Note：topic partitions are assigned to tasks, and tasks are assigned to all threads over all instances, in a best-effort attempt to trade off load-balancing and stickiness of stateful tasks. For this assignment, Kafka Streams uses the [StreamsPartitionAssignor][https://github.com/apache/kafka/blob/trunk/streams/src/main/java/org/apache/kafka/streams/processor/internals/StreamsPartitionAssignor.java] class and doesn't let you change to a different assignor. If you try to use a different assignor, Kafka Streams ignores it.

```
将主题分区分配给任务，并将任务分配给所有实例的所有线程。尽最大努力尝试权衡有状态任务的负载平衡和粘性。对于此分配，Kafka Streams使用 StreamsPartitionAssignor 类，并且不允许你更改为其他分配器，如果你尝试使用其他分配器，则Kafka Streams会忽略它
```

The following diagram shows two tasks each assigned with open partition of the input streams.

![img](http://kafka.apache.org/28/images/streams-architecture-tasks.jpg)

## Threading Model

Kafka Streams allows the user to configure the number of threads that the library can use ti parallelize processing within an application instance. Each thread can execute one or more tasks with their processor topologies independently. For example, the following diagram shows one stream thread running two stream tasks.

```
Kafka Streams 允许用户配置可用于并行处理应用程序实例中的处理的线程数。每个线程可以使用其处理器拓扑独立执行一个或多个任务。例如：下图展示了一个流线程允许两个流任务。
```

![img](http://kafka.apache.org/28/images/streams-architecture-threads.jpg)

Starting more stream threads or more instances of the application merely amounts to replicating the topology and having it process a different subset of Kafka partitions, effectively parallelizing processing.It is worth noting that there is no shared state amongst the threads, so no inter-thread  coordination is necessary. This makes it very simple to run topologies in parallelism acroess the application instances and thread. The assignment of Kafka topic partitions amongst the various stream thread is transparently handled by Kafka Stream leveraging [Kafka's coordination][https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Client-side+Assignment+Proposal] functionality.

```
开启多个流线程获取多个应用程序实例仅仅相当于复制多个拓扑结构并使其处理Kafka分区的不同子集，从而有效的并行处理。值得注意的是，它们没有共享其线程中的状态，所以不需要线程间的协调，这使得跨应用程序实例和线程并行运行拓扑非常简单。Kafka Streams 利用Kafka的协调功能来透明地处理各个流线程之间的Kafka主题分区分配。
```

As we described above, scaling you stream processing application with Kafka Streams is easy: you merely need to start additional instances of you application, and Kafka Streams takes care of distributing partitions amongst tasks that run in the application instances. You can start as many threads of the application as there are input Kafka topic partition so that. across all running instances of an application, every thread(or rather, the tasks it runs) has at least one input partition to process.

```
正如我们上面说的：用Kafka Stream 扩展你的流处理程序是简单的。你仅仅需要开启额外的应用程序实例，Kafka Streams 就会在应用程序实例中运行的任务之间分配分区。你可以启动与输入Kafka主题分区一样多的应用程序线程，以便在应用程序的所有正在运行实例中，每个线程至少具有一个要处理的输入分区。
```

As of Kafka 2.8 you can scale stream threads much in the same way you can scale your Kafka Stream clients. Simply add or remove stream threads and Kafka Streams will take care of redistributing the partitions. you may also add threads to replace stream threads that have died removing the need to restart clients to recover the number of thread running.

```
在2.8版本后，你可以以扩展KafkaStream客户端相同的方式扩展流程序。简单的添加或一处stream线程，Kafka Streams将负责重新分配分区。你也可以提那家线程来替换已死的steam线程，从而无需重新启动客户端以恢复正在运行的线程数。
```



