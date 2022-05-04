import json

from kafka import KafkaConsumer
from psycopg2 import extras
import db as DB
from helper import extract_dash_strings

try:
    consumer = KafkaConsumer(
        'mytopic',
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
       group_id='my-group-id',
       value_deserializer=lambda m: json.loads(m.decode('ascii')))

    db_instance = DB.get_db()
        
except Exception as e:
    print(e)



batch_views = []

for message in consumer:

    ts = message.timestamp
    val = json.loads(message.value)

    batch_views.append(
        {'user_id': extract_dash_strings(val['userid']), 'event': val['event'], 'source': val['context']['source'],
         'timestamp': ts, 'product_id': extract_dash_strings(val['properties']['productid'])})

    if len(batch_views) == 100:
        with db_instance.cursor()as cursor:
            try:
                iter_views = ({**view} for view in batch_views)

                extras.execute_batch(cursor, """
                    INSERT INTO user_views(user_id, user_event, user_event_source, user_event_date, product_id) VALUES (
                        %(user_id)s,
                        %(event)s,
                        %(source)s,
                        %(timestamp)s,
                        %(product_id)s
                    );
                """, iter_views)

                print(val['userid'], val['event'], val['context']['source'], val['properties']['productid'], ts)
            except (Exception) as error:
                db_instance.rollback()
                raise Exception(f"DB update failed. Reason: {error}")
            finally:
                cursor.close()
                db_instance.commit()
                batch_views = []

