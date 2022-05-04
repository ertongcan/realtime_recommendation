import os
from psycopg2 import connect, extras
from dotenv import load_dotenv

load_dotenv()
db_instance = connect(
    f"dbname='{os.environ.get('DBNAME')}' user='{os.environ.get('DBUSER')}' host='{os.environ.get('DBHOST')}' password='{os.environ.get('DBPASS')}' port='{os.environ.get('DBPORT')}'")


def transform():
    with db_instance.cursor(cursor_factory=extras.RealDictCursor) as cursor:
        try:
            qSelect = """ select o.user_id, p.category_id, p.product_id, count(1) from orders o, order_items oi, products p where o.order_id = oi.order_id and p.product_id = oi.product_id group by o.user_id, p.category_id, p.product_id order by 4 DESC LIMIT 10
 """
            cursor.execute(qSelect)
            best_seller_categories = cursor.fetchall()


        except (Exception) as error:
            db_instance.rollback()
            raise Exception(f"DB query failed. Reason: {error}")
        finally:
            cursor.close()
            db_instance.commit()

    return best_seller_categories if best_seller_categories is not None else best_seller_categories

def load(bs):
    try:
        with db_instance.cursor() as cursor:
            iter_views = ({'user_id': view['user_id'], 'product_id': view['product_id']} for view in bs)

            return extras.execute_batch(cursor, """
                                INSERT INTO recommended_user_products(user_id, product_id) VALUES (
                                    %(user_id)s,
                                    %(product_id)s
                                );
                            """, iter_views, page_size=100) if bs is not None else False


    except (Exception) as error:
        db_instance.rollback()
        raise Exception(f"DB query failed. Reason: {error}")
    finally:
        cursor.close()
        db_instance.commit()



try:
    best_sellers = transform()
    if best_sellers:
        # write to db
        load(best_sellers)


except Exception as e:
    print(e)



