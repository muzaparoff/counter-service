from gevent.pywsgi import WSGIServer

import asyncio
from flask import Flask, request
import pika

app = Flask(__name__)
counter = 0

# RabbitMQ connection parameters
rabbitmq_host = 'localhost'
rabbitmq_queue = 'counter_queue'

# Function to increment the counter and publish to RabbitMQ
async def increment_counter():
    global counter
    counter += 1

    # Create a connection to RabbitMQ
    connection = pika.AsyncioConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = await connection.channel()

    # Declare the queue (create if it doesn't exist)
    await channel.queue_declare(queue=rabbitmq_queue)

    # Publish the updated counter value to RabbitMQ
    await channel.basic_publish(
        exchange='',
        routing_key=rabbitmq_queue,
        body=str(counter),
    )

    # Close the RabbitMQ connection
    await connection.close()

@app.route('/', methods=['GET', 'POST'])
def counter_service():
    if request.method == 'POST':
        # Increment the counter asynchronously
        asyncio.ensure_future(increment_counter())

    return f'Counter: {counter}'

if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()