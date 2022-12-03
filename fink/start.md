在docker 上运行flink 的session 集群模式

1. 创建docker 网络

   ```sh
   docker network create flink-network
   ```

   

2. 输入系统环境变量 

   ```
   FLINK_PROPERTIES="jobmanager.rpc.address: jobmanager"
   ```

3. 启动jobmanager

   ```sh
   docker run --rm --name jobmanager --network flink-network --publish 8081:8081 --env FLINK_PROPERTIES="jobmanager.rpc.address: jobmanager" flink:latest jobmanager
   ```

4. 启动多个taskmanager

   ```sh
    docker run --rm --name=taskmanager-0 --network=flink-network --env FLINK_PROPERTIES="jobmanager.rpc.address: jobmanager" flink:latest taskmanager 
   ```

   

