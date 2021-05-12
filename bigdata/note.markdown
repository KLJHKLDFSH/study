

# HDFS 和 Hive 和 HBase 的关系

>HDFS 用于数据存储  
>Hive 使用MapReduce查询存储与HDFS上的数据，查询速度较慢，时效性很低，但提供了类SQL语句的HQL。适合用于大量数据的分析。（例如每日的数据统计）。   
>HBase 提供实时查询存储在HDFS上的数据，但仅提供了Java接口。如果需要使用SQL语言进行操作需要配合其他框架 如:Hive,impala,Phoneix，如果搭配Hive,那么在实时性上会有一定的损失。

> 总结： HDFS作为数据存储底层，Hive 和 HBase都是建立在HDFS之上，用于查询存储在HDFS上的数据，但是Hbase有时需要使用SQL时会搭配Hive使用。