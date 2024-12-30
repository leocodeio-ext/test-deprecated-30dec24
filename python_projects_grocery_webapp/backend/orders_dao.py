from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    cursor = connection.cursor()

    order_query = """
        INSERT INTO orders (customer_name, total, datetime)
        VALUES (?, ?, ?)
    """
    order_data = (order['customer_name'], order['grand_total'], datetime.now())

    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    order_details_query = """
        INSERT INTO order_details (order_id, product_id, quantity, total_price)
        VALUES (?, ?, ?, ?)
    """

    order_details_data = []
    for order_detail in order['order_details']:
        order_details_data.append((
            order_id,
            int(order_detail['product_id']),
            float(order_detail['quantity']),
            float(order_detail['total_price'])
        ))
    
    cursor.executemany(order_details_query, order_details_data)
    connection.commit()

    return order_id

def get_order_details(connection, order_id):
    cursor = connection.cursor()

    query = """
        SELECT order_details.order_id, order_details.quantity, 
               order_details.total_price, products.name, 
               products.price_per_unit 
        FROM order_details 
        LEFT JOIN products ON order_details.product_id = products.product_id 
        WHERE order_details.order_id = ?
    """

    cursor.execute(query, (order_id,))

    records = []
    for row in cursor:
        records.append({
            'order_id': row['order_id'],
            'quantity': row['quantity'],
            'total_price': row['total_price'],
            'product_name': row['name'],
            'price_per_unit': row['price_per_unit']
        })

    return records

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM orders")
    cursor.execute(query)
    response = []
    for (order_id, customer_name, total, dt) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': dt,
        })

    cursor.close()

    # append order details in each order
    for record in response:
        record['order_details'] = get_order_details(connection, record['order_id'])

    return response

if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))
    # print(get_order_details(connection,4))
    # print(insert_order(connection, {
    #     'customer_name': 'dhaval',
    #     'total': '500',
    #     'datetime': datetime.now(),
    #     'order_details': [
    #         {
    #             'product_id': 1,
    #             'quantity': 2,
    #             'total_price': 50
    #         },
    #         {
    #             'product_id': 3,
    #             'quantity': 1,
    #             'total_price': 30
    #         }
    #     ]
    # }))