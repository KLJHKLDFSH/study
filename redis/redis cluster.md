# Redis Cluster

```shell

./src/redis-server cluster/redis-7000.conf 
./src/redis-server cluster/redis-7001.conf 
./src/redis-server cluster/redis-7002.conf 
./src/redis-server cluster/redis-7003.conf 

redis-cli --cluster create 127.0.0.1:17000 127.0.0.1:17001 127.0.0.1:17002 127.0.0.1:17003 --cluster-replicas 1

```

