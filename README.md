# Realtime Recommendation Service

- Running the kafka and zookeeper on the docker container

### Installation

```sh
cd <PROJECT_FOLDER>
docker-compose -f docker-compose.yml up -d

to tear down docker RUN:
docker-compose -f docker-compose.yml down

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
#### ENDPOINTS
```sh
/browse_history/<string:user_id>
/delete_history/<string:user_id>/<string:product_id>
/best_seller_products/<string:user_id>
```
#### for db tables please run tables.sql
