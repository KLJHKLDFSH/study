# TCP and UDP support

#### maven:

```xml
<dependency>
    <groupId>org.springframework.integration</groupId>
    <artifactId>spring-integration-ip</artifactId>
    <version>5.5.0</version>
</dependency>
```



### Introduction

#### UDP

Two flavors each of UDP inbound and outbound channel adapters are provided:

- `UnicastSendingMessageHandler` sends a datagram packet to a single destination.
- `UnicastReceivingChannelAdapter` receives incoming datagram packets.
- `MulticastSendingMessageHandler` sends (broadcasts) datagram packets to a multicast address.
- `MulticastReceivingChannelAdapter` receives incoming datagram packets by joining to a multicast address.

#### TCP

Tcp inbound and outbound channel adapters are provided:

- `TcpSendingMessageHandler` sends messages over TCP.
- `TcpReceivingChannelAdapter` receives messages over TCP.



### UDP Adapters

UDP is an efficient but unreliable protocol. Spring Integration adds two attributes to improve reliability: `check-length` and `acknowledge`. 

- check-length 

  - 在消息数据之前添加一个数据长度字段（4 bytes），使接收站点可以验证数据长度。如果接收方使用的 `buffer`太短无法容纳整个数据包，这个数据包会被阶段，`length` header 提供了机制去检测这种情况。

    ```
    The recipient of the packet must also be configured to expect a length to precede the actual data. For a Spring Integration UDP inbound channel adapter, set its check-length attribute.
    ```

    

- acknowledge 

  - 运行在接收到消息后，在指定的时间内回复发生者
  - 设置 acknowledge = true 之后，意味着包的接受者可以解析被添加在报文头中包含着acknowledgment 数据（host 和 port）
  - 多播时，附加属性(min-acks-for- success) 指定在 `ack-timeout`内必须接收多少确认



#### Version Features

Starting with version 4.3, you can set the `port` to `0`, in which case the operating system chooses the port. <u>The chosen port can be discovered by invoking `getPort()` after the adapter is started and `isListening()` returns `true`.</u>

Starting with version 4.3, you can set the `ackPort` to `0`, in which case the operating system chooses the port.

Starting with version 5.3.3, you can add a `SocketCustomizer` bean to modify the `DatagramSocket` after it is created (for example, call `setTrafficClass(0x10)`).



#### Outbound UDP Adapters Configuration

###### JAVA Configuration

```java
//unicast
@Bean
@ServiceActivator(inputChannel = "udpOut")
public UnicastSendingMessageHandler handler(){ 
   return new UnicastSendingMessageHandler("localhost",11111);
}

//multicase
@Bean
@ServiceActivator(inputChannel = "udpOut")
public MulticastSendingMessageHandler handler(){ 
   return new MulticastSendingMessageHandler("localhost",11111);
}

```



###### Java DSL Configuration

```java
@Bean
public IntegrationFlow udpOutFlow()}{
    return f -> f.handle(Udp.outboundAdapter("localhost",12345)
                .configureSocket(socket-> socket.setTrafficClass(0x10)))
        		.get();
}
```





#### Inbound UDP Adapters

默认情况下，对入栈数据包进行反向DNS查找，以将IP地址转换为主机名以用于消息头。在未配置DNS的环境中，可能会导致延迟。可以通过将`lookup-host`设置为`false`来覆盖这个默认行为。

Starting with version 5.3.3, you can add a `SocketCustomizer` bean to modify the `DatagramSocket` after it is created. It is called for the receiving socket and any sockets created for sending acks.



###### Inbound UDP Adapters

**Java Configuration**

```java
@Bean
public UnicastReceivingChannelAdapter udpIn(){
    UnicastReceivingChannelAdapter adapter = 
        new UnicastReceivingChannelAdapter();
    adapter.setOutputChannelName("udpChannel");
    return adapter;
}
```



**Java DSL Configuration**

```java
@Bean
public IntegrationFlow udpIn(){
    return IntegrationFlows.from(Udp.inboundAdapter(12345))
        .channel("udpChannel")
        .get();
}
```



#### Advanced Outbound Configuration



###### UnicastSendingMessageHandler 

- `destination-expression`

  ​	使用`destination-expression`作为硬编码`host`-`port` 对在运行时的替代方案，以确定针对`requestMessage`的传出数据包数据包的目标地址

  - `URL`
  - `SocketAddress`
  - `IpHeaders.PACKET_ADDRESS`

  `DatagramPacket.getSocketAddress()`可以精确的获取到`SocketAddress`

  

- `socket-expression`

- 

**Java DSL Configuration**

```java
@Bean
public IntegrationFlow udpEchoUpcaseServer(){
    return IntegrationFlow.from(Udp.inboundAdapter(12345).id("udpIn"))
        .<byte[],String>transform(p -> new String(p).toUpperCase())
        .handle(Udp.outboundAdapter("headers['ip_packetAddress']")
                .socketExpression("@udpIn.socket"))
        .get();
}
```

























