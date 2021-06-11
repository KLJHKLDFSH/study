

# Using Kafka Streams

-To catch any unexpected exceptions, you can set an `java.lang.Thread.UncaughtExceptionHandler`

```java
streams.setUncaughtExceptionHandler((Thread thread, Throwable throwable) -> {
  // here you should examine the throwable/exception and perform an appropriate action!
});

```



# Processor Api

