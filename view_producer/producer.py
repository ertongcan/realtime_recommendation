import json
from time import sleep
from kafka import KafkaProducer

def on_send_success(record_metadata):

    print(record_metadata)
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

def on_send_error(excp):
    # TODO log, send email etc.
    print(f'err - {excp}')

producer = KafkaProducer(bootstrap_servers=['kafka:9092'],value_serializer=lambda m: json.dumps(m).encode('ascii'))

lines = []
with open('product-views.json') as f:
    lines = f.readlines()
    for line in lines:
        producer.send(topic='mytopic', value=line).add_callback(on_send_success).add_errback(on_send_error)
        sleep(1)
