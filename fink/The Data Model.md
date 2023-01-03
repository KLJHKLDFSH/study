# 								数据流模型



## 概念上的统一模型

### 概念

- Allow for the calculation of event-time ordered results, `windowed` by features of the data themselves, over an **<u>unbounded</u>**, **<u>unordered</u>** data source, with **<u>correctness</u>**, **<u>latency</u>**, and <u>**cost tunable**</u> across a broad spectrum of combinations

- Decomposes pipeline implementation across four related dimensions, providing **<u>clarity</u>**, **<u>composability</u>**, and <u>**flexibility**</u>
  - **What** results is being computed
  - **Where** in event time they are being computed
  - **When** in processing time they are materialized
  - **How** earlier results relate to later refinement.
- **<u>Separates the logical notion of data processing from the underlying physical implementation</u>**, allowing the choice of batch, micro-batch, or streaming engine to become one of simply correctness, latency, and cost

### 大纲：

- ***A windowing model*** which supports unaligned event-time windows
- **<u>A triggering model</u>** that binds the output times of results to runtime characteristics of the pipeline,
- **<u>An Incremental processing model</u>** that integrates retractions and updates into the windowing and triggering model described above
- Scalable implementations of the above atop the MillWheel streaming engine and the FlumeJava batch engine
- A set of core principles the guided the design of this model
- Brief discussions of our real-world experiences with massive-scale,unbounded,out-of-order data processing as Google that motivated development of this model.



### Unbounded/Bounded vs Streaming/Batch

​	Streaming/batch 在语义上有暗示使用特定执行引擎的含义。



### Windowing



