import asyncio
from quart import Quart, request
import aio_pika
import logging
import sqlite3
import time

logging.basicConfig(level=logging.INFO)

app = Quart(__name__)
counter = 0

# RabbitMQ connection parameters
rabbitmq_host = 'localhost'
rabbitmq_queue = 'counter_queue'

# SQLite database file
db_file = '/app/data/counter.db'

def set_db_file(path):
    global db_file
    db_file = path

def init_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS counter (
            id INTEGER PRIMARY KEY,
            value INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO counter (id, value) VALUES (1, 0)
    ''')
    conn.commit()
    conn.close()

def get_counter_from_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM counter WHERE id = 1')
    value = cursor.fetchone()[0]
    conn.close()
    return value

def update_counter_in_db(value):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('UPDATE counter SET value = ? WHERE id = 1', (value,))
    conn.commit()
    conn.close()

# Function to increment the counter and publish to RabbitMQ
async def increment_counter():
    logging.info('Incrementing counter')
    global counter
    counter += 1
    update_counter_in_db(counter)
    logging.info(f'Counter: {counter}')

    for _ in range(5):  # Retry up to 5 times
        try:
            # Create a connection to RabbitMQ
            logging.info('Creating connection to RabbitMQ')
            connection = await aio_pika.connect_robust(host=rabbitmq_host)
            logging.info('Connection created')
            channel = await connection.channel()
            logging.info('Channel created')

            # Declare the queue (create if it doesn't exist)
            await channel.declare_queue(rabbitmq_queue)
            logging.info('Queue declared')

            # Publish the updated counter value to RabbitMQ
            await channel.default_exchange.publish(
                aio_pika.Message(body=str(counter).encode()),
                routing_key=rabbitmq_queue,
            )
            logging.info('Message published')
            return
        except aio_pika.exceptions.AMQPConnectionError as e:
            logging.error(f'Error connecting to RabbitMQ: {e}')
            time.sleep(5)  # Wait for 5 seconds before retrying
        except Exception as e:
            logging.error(f'An unexpected error occurred: {e}')
            return

async def consume_counter():
    for _ in range(5):  # Retry up to 5 times
        try:
            # Create a connection to RabbitMQ
            logging.info('Creating connection to RabbitMQ')
            connection = await aio_pika.connect_robust(host=rabbitmq_host)
            logging.info('Connection created')
            channel = await connection.channel()

            # Perform consuming logic here
            # ...

            return channel
        except aio_pika.exceptions.AMQPConnectionError as e:
            logging.error(f'Error connecting to RabbitMQ: {e}')
            time.sleep(5)  # Wait for 5 seconds before retrying
        except asyncio.TimeoutError as e:
            logging.error(f'Timeout error: {e}')
            time.sleep(5)  # Wait for 5 seconds before retrying
        except Exception as e:
            logging.error(f'An unexpected error occurred: {e}')
            return
        finally:
            # Close the RabbitMQ connection
            if connection and not connection.is_closed:
                await connection.close()
                logging.info('Connection closed')

@app.route('/', methods=['GET', 'POST'])
async def counter_service():
    logging.info('Counter service called')
    if request.method == 'POST':
        await increment_counter()
    return f'''
    <html>
        <body>
            <h1>Counter: {counter}</h1>
            <form method="post">
                <button type="submit">Increment Counter</button>
            </form>
        </body>
    </html>
    '''

if __name__ == "__main__":
    logging.info('Starting counter service')

    # Initialize the database
    init_db()

    # Restore the counter value from the database
    counter = get_counter_from_db()
    logging.info(f'Restored counter value: {counter}')

    # Start the asyncio event loop
    loop = asyncio.get_event_loop()

    # Use an async WSGI server to handle async routes
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:5000"]
    loop.run_until_complete(serve(app, config))