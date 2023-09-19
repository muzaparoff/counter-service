import unittest
import asyncio
from unittest.mock import Mock, patch
from counter_service import app
import pika

class TestCounterService(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Initialize Flask app for testing
        self.app = app.test_client()

        # Create a mock RabbitMQ connection and channel for testing
        self.mock_connection = Mock()
        self.mock_channel = Mock()

        async def mock_connection():
            return self.mock_connection

        async def mock_channel():
            return self.mock_channel

        # Patch pika's asynchronous methods
        with patch('pika.AsyncioConnection', mock_connection), \
             patch('pika.AsyncioChannel', mock_channel):
            await self.asyncSetUpRabbitMQ()

    async def asyncSetUpRabbitMQ(self):
        # Your RabbitMQ setup code here (if any)

    async def asyncTearDown(self):
        # Clean up resources and connections
        await self.app.close()
        await self.mock_connection.close()

    async def test_post_request_increments_counter(self):
        # Simulate a POST request to increment the counter
        response = await self.app.post('/')
        self.assertEqual(response.status_code, 200)

        # Simulate a GET request to retrieve the counter value
        response = await self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Counter: 1', response.data)

    async def test_multiple_post_requests(self):
        # Simulate multiple POST requests to increment the counter
        for _ in range(5):
            response = await self.app.post('/')
            self.assertEqual(response.status_code, 200)

        # Simulate a GET request to retrieve the counter value
        response = await self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Counter: 5', response.data)

if __name__ == '__main__':
    unittest.main()
