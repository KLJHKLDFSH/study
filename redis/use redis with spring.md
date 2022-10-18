### Hash Mapper

- Direct mapping, by using HashOperations and a seruakuzer
- Using Redis Respositories
- User HashMapper and HashOperations



#### Hash Mappers

​	Hash mappers are converters of map objects to a `Map<K, V>` and back. `HashMapper` is intended for using with Redis Hashes.

Multiple implementations are available:

- `BeanUtilsHashMapper` using Spring’s [BeanUtils](https://docs.spring.io/spring/docs/5.3.9/javadoc-api/org/springframework/beans/BeanUtils.html).
- `ObjectHashMapper` using [Object-to-Hash Mapping](https://docs.spring.io/spring-data/redis/docs/2.4.11/reference/html/#redis.repositories.mapping).
- [`Jackson2HashMapper`](https://docs.spring.io/spring-data/redis/docs/2.4.11/reference/html/#redis.hashmappers.jackson2) using [FasterXML Jackson](https://github.com/FasterXML/jackson).

Example:

```java
public class Person {
  String firstname;
  String lastname;

  // …
}

public class HashMapping {

  @Autowired
  HashOperations<String, byte[], byte[]> hashOperations;

  HashMapper<Object, byte[], byte[]> mapper = new ObjectHashMapper();

  public void writeHash(String key, Person person) {

    Map<byte[], byte[]> mappedHash = mapper.toHash(person);
    hashOperations.putAll(key, mappedHash);
  }

  public Person loadHash(String key) {

    Map<byte[], byte[]> loadedHash = hashOperations.entries("key");
    return (Person) mapper.fromHash(loadedHash);
  }
}
```





#### Jackson2HashMappe

`Jackson2HashMapper` can map top-level properties as Hash field names and, optionally, flatten the structure.

Example:

```java
public class Person {
  String firstname;
  String lastname;
  Address address;
  Date date;
  LocalDateTime localDateTime;
}

public class Address {
  String city;
  String country;
}
```



Normal Mapping

| Hash Field    | Value                                                  |
| :------------ | :----------------------------------------------------- |
| firstname     | `Jon`                                                  |
| lastname      | `Snow`                                                 |
| address       | `{ "city" : "Castle Black", "country" : "The North" }` |
| date          | `1561543964015`                                        |
| localDateTime | `2018-01-02T12:13:14`                                  |

Flat Mapping

| Hash Field      | Value                 |
| :-------------- | :-------------------- |
| firstname       | `Jon`                 |
| lastname        | `Snow`                |
| address.city    | `Castle Black`        |
| address.country | `The North`           |
| date            | `1561543964015`       |
| localDateTime   | `2018-01-02T12:13:14` |



### Redis Transactions

​		Redis provides support for [transactions](https://redis.io/topics/transactions) through the `multi`, `exec`, and `discard` commands. These operations are available on `RedisTemplate`. However, `RedisTemplate` is not guaranteed to run all the operations in the transaction with the same connection.



#### SessionCallback

Example:

```java
//execute a transaction
List<Object> txResults = redisTemplate.execute(new SessionCallback<List<Object>>() {
  public List<Object> execute(RedisOperations operations) throws DataAccessException {
    operations.multi();
    operations.opsForSet().add("key", "value1");

    // This will contain the results of all operations in the transaction
    return operations.exec();
  }
});
System.out.println("Number of items added to set: " + txResults.get(0));
```





### Pipelineing

Pipelinine can improve performance when you need to send several commands in a row, such as adding many elements to the same List.



Srping Data Redis provides several `RedisTemplate` methods for runnng commands in a pipeline.

- standard execute method

- `executePipelined` methods run the provided `RedisCallback` or `sessuinCallback` in a pipeline and return the results,

  Example:

  ```java
  //pop a specified number of items from a queue
  List<Object> results = stringRedisTemplate.executePipelined(
    new RedisCallback<Object>() {
      public Object doInRedis(RedisConnection connection) throws DataAccessException {
        StringRedisConnection stringRedisConn = (StringRedisConnection)connection;
        for(int i=0; i< batchSize; i++) {
          stringRedisConn.rPop("myqueue");
        }
      return null;
    }
  });
  ```

  

