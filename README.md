# Kafka Producer and Consumer using docker and docker-compose example

- Running the kafka and zookeeper on the docker container

### Installation

```sh
$ docker-compose up -d
```

#### It will start producing the messages and push to the kafka
```sh
$ cd producer
$ ./build.sh
$ ./start.sh
```

#### It will start receiving the messages from kafka and process the messages
```sh
$ cd consumer
$ ./build.sh
$ ./start.sh
```

#### ETL process to create warehouse table
```sh
$ cd etl
$ ./build.sh
$ ./start.sh
```

#### API to use recommendation service
```sh
$ cd api
$ ./build.sh
$ ./start.sh
```

#### for db tables please run tables.sql
