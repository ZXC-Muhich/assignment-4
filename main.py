import uuid
import random
import psycopg2
import psycopg2.extras
from psycopg2 import Error
from faker import Faker

fake = Faker()

HOST = 'localhost'
USER = 'postgres'
PASSWORD = '290408'
DATABASE = 'mcdonalds'
PORT = '5432'


def create_connection():
    try:
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            dbname=DATABASE,
        )
        print("Connection to PostgreSQL DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None


def execute_batch_query(connection, query, data):
    try:
        with connection.cursor() as cursor:
            psycopg2.extras.execute_values(cursor, query, data)
        connection.commit()
    except Error as e:
        connection.rollback()
        print(f"The error '{e}' occurred")


def insert_data():
    connection = create_connection()
    if connection is None:
        return

    restaurants_query = """
                        INSERT INTO restaurants (id, location_name, address, is_drive_thru)
                        VALUES %s ON CONFLICT (id) DO NOTHING \
                        """
    restaurants_data = [
        (str(uuid.uuid4()), "McDonalds Khreshchatyk", "Khreshchatyk St, 19, Kyiv", True),
        (str(uuid.uuid4()), "McDonalds Vokzalna", "Vokzalna Square, 1, Kyiv", False),
        (str(uuid.uuid4()), "McDonalds KSE Campus", "Mykoly Shpaka St, 3, Kyiv", False),
        (str(uuid.uuid4()), "McDonalds Dnipro Center", "Yavornytskoho Ave, 50, Dnipro", True)
    ]
    print("Inserting restaurants...")
    execute_batch_query(connection, restaurants_query, restaurants_data)

    menu_query = """
                 INSERT INTO menu_items (id, name, category, price, calories)
                 VALUES %s ON CONFLICT (id) DO NOTHING \
                 """
    menu_data = [
        (str(uuid.uuid4()), "Big Mac", "Burgers", 120.00, 508),
        (str(uuid.uuid4()), "Cheeseburger", "Burgers", 60.00, 300),
        (str(uuid.uuid4()), "McChicken", "Burgers", 105.00, 400),
        (str(uuid.uuid4()), "French Fries (M)", "Sides", 65.00, 340),
        (str(uuid.uuid4()), "McNuggets (6 pc)", "Snacks", 90.00, 250),
        (str(uuid.uuid4()), "Coca-Cola (M)", "Drinks", 45.00, 150),
        (str(uuid.uuid4()), "Latte", "Cafe", 60.00, 120),
        (str(uuid.uuid4()), "McFlurry Oreo", "Desserts", 85.00, 380)
    ]
    print("Inserting menu items...")
    execute_batch_query(connection, menu_query, menu_data)

    customers_query = """
                      INSERT INTO customers (id, first_name, last_name, email, phone)
                      VALUES %s ON CONFLICT (email) DO NOTHING \
                      """
    customers_data = []
    print("Generating 1000 customers...")
    for _ in range(1000):
        customers_data.append((
            str(uuid.uuid4()),
            fake.first_name(),
            fake.last_name(),
            fake.unique.email(),
            fake.phone_number()[:20]
        ))
    execute_batch_query(connection, customers_query, customers_data)

    loyalty_query = """
                    INSERT INTO loyalty_cards (id, customer_id, points, issue_date)
                    VALUES %s ON CONFLICT (customer_id) DO NOTHING \
                    """
    loyalty_data = []
    print("Generating 500 loyalty cards...")
    for i in range(500):
        loyalty_data.append((
            str(uuid.uuid4()),
            customers_data[i][0],
            random.randint(0, 1500),
            fake.date_between(start_date='-2y', end_date='today')
        ))
    execute_batch_query(connection, loyalty_query, loyalty_data)

    orders_query = """
                   INSERT INTO orders (id, restaurant_id, customer_id, order_date, total_amount, status)
                   VALUES %s ON CONFLICT (id) DO NOTHING \
                   """
    order_items_query = """
                        INSERT INTO order_items (order_id, menu_item_id, quantity, item_price)
                        VALUES %s ON CONFLICT (order_id, menu_item_id) DO NOTHING \
                        """

    statuses = ['Pending', 'Completed', 'Cancelled']
    total_orders = 500000
    batch_size = 10000
    batches = total_orders // batch_size

    print(f"Generating {total_orders} transaction records in {batches} batches...")

    for batch_num in range(batches):
        orders_data = []
        order_items_data = []

        for _ in range(batch_size):
            order_id = str(uuid.uuid4())
            rest_id = random.choice(restaurants_data)[0]

            cust_id = random.choice(customers_data)[0] if random.random() > 0.2 else None
            order_date = fake.date_time_between(start_date='-1y', end_date='now')
            status = random.choices(statuses, weights=[0.05, 0.9, 0.05])[0]

            num_items = random.randint(1, 4)
            chosen_menu_items = random.sample(menu_data, num_items)

            total_amount = 0
            for item in chosen_menu_items:
                quantity = random.randint(1, 3)
                item_price = item[3]
                total_amount += quantity * item_price

                order_items_data.append((
                    order_id,
                    item[0],
                    quantity,
                    item_price
                ))

            orders_data.append((
                order_id,
                rest_id,
                cust_id,
                order_date,
                total_amount,
                status
            ))

        execute_batch_query(connection, orders_query, orders_data)
        execute_batch_query(connection, order_items_query, order_items_data)

        print(f"Batch {batch_num + 1}/{batches} completed. ({(batch_num + 1) * batch_size} orders inserted)")

    connection.close()
    print("All data generated and inserted successfully! Connection closed.")


if __name__ == "__main__":
    insert_data()