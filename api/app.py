from flask import Flask,jsonify, make_response
from psycopg2 import connect, extras

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['db'] = connect(
            f"dbname='{os.environ.get('DBNAME')}' user='{os.environ.get('DBUSER')}' host='{os.environ.get('DBHOST')}' password='{os.environ.get('DBPASS')}' port='{os.environ.get('DBPORT')}'")


@app.route('/')
def index():
    return ''

@app.route('/delete_history/<string:user_id>/<string:product_id>', methods=['DELETE'])
def delete_history(user_id, product_id):
    db_instance = app.config['db'] if 'db' in app.config else None

    if db_instance:
        with db_instance.cursor() as cursor:
            try:
                qSelect = """ DELETE from user_views WHERE user_id=%s and product_id=%s """
                cursor.execute(qSelect, (user_id,product_id, ))
            except (Exception) as error:
                db_instance.rollback()
                raise Exception(f"DB operation failed. Reason: {error}")
            finally:
                cursor.close()
                db_instance.commit()

@app.route('/browse_history/<string:user_id>')
def browse_history(user_id):
    db_instance = app.config['db'] if 'db' in app.config else None

    if db_instance:
        with db_instance.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            try:
                qSelect = """ select * from user_views uv where uv.user_id = %s ORDER BY user_event_date DESC;"""
                cursor.execute(qSelect, (user_id,))
                history = cursor.fetchall()
                json_res = {'user_id': user_id, 'products': [p['product_id'] for p in history],
                            'type': 'personalized'}

            except (Exception) as error:
                db_instance.rollback()
                return make_response(jsonify(f"DB failed - {error}"), 200)
            finally:
                cursor.close()
                db_instance.commit()
    return make_response(jsonify(json_res), 200)

@app.route('/best_seller_products/<string:user_id>', methods=['GET'])
def best_seller_products(user_id):
    db_instance = app.config['db'] if 'db' in app.config else None

    if db_instance:
        with db_instance.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            try:
                # check for history
                qSelect = """ select * from user_views uv where uv.user_id = %s """
                cursor.execute(qSelect, (user_id,))
                history = cursor.fetchall()

                if len(history) > 0:
                    print("here")
                    qSelect = """ select * from recommended_user_products rup where rup.user_id = %s LIMIT 5"""
                    cursor.execute(qSelect, (user_id, ))
                    best_seller_categories = cursor.fetchall()


                    if len(best_seller_categories) >= 5:
                        json_res = {'user_id':user_id, 'products':[p['product_id'] for p in best_seller_categories], 'type':'personalized'}
                        return make_response(jsonify(json_res), 200)
                    else:
                        return make_response(jsonify([]), 200)
                else:

                    qSelect = """ select o.user_id, p.product_id, count(1) from orders o, order_items oi, products p where o.order_id = oi.order_id and p.product_id = oi.product_id group by o.user_id, p.product_id order by 3 DESC LIMIT 5; """
                    cursor.execute(qSelect, (user_id,))
                    general_best_sellers = cursor.fetchall()
                    if len(general_best_sellers) >= 5:
                        json_res = {'user_id': user_id, 'products': [p['product_id'] for p in general_best_sellers],
                                'type': 'non-personalized'}
                        return make_response(jsonify(json_res), 200)
                    else:
                        return make_response(jsonify([]), 200)
            except (Exception) as error:
                db_instance.rollback()
                raise Exception(f"DB update failed. Reason: {error}")
            finally:
                cursor.close()
                db_instance.commit()
    else:
        return make_response(f"DB connection problem", 500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)