import time

from psycopg2 import connect


import logging


def get_db():
    while True:
        try:

            db_ins = connect(
                "dbname='postgres' user='postgres' host='postgres' password='123456' port='5432'")

            return db_ins
        except Exception as e:
            logging.error(f"Could not connect to db pool! Reason:{e}")
            time.sleep(3)
            continue