import unittest
import asyncio
from unittest.mock import AsyncMock, patch
from quart import Quart
from counter_service import app, init_db, update_counter_in_db, get_counter_from_db

class TestCounterService(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Initialize Quart app for testing
        self.app = app.test_client()
        self.app.testing = True

        # Use an in-memory SQLite database for testing
        global db_file
        db_file = ':memory:'
        init_db()

        # Create a mock RabbitMQ connection and channel for testing
        self.mock_connection = AsyncMock()
        self.mock_channel = AsyncMock()

        async def mock_connect_robust(*args, **kwargs):
            return self.mock_connection

        async def mock_channel_method():
            return self.mock_channel

        # Patch aio_pika's asynchronous methods
        patcher1 = patch('aio_pika.connect_robust', mock_connect_robust)
        patcher2 = patch('aio_pika.RobustChannel', mock_channel_method)
        self.addCleanup(patcher1.stop)
        self.addCleanup(patcher2.stop)
        patcher1.start()
        patcher2.start()

    async def asyncTearDown(self):
        # Clean up resources and connections
        await self.mock_connection.close()

    async def test_post_request_increments_counter(self):
        # Simulate a POST request to increment the counter
        async with self.app as client:
            response = await client.post('/')
            self.assertEqual(response.status_code, 200)

            # Simulate a GET request to retrieve the counter value
            response = await client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Counter: 1', await response.get_data())

    async def test_multiple_post_requests(self):
        # Simulate multiple POST requests to increment the counter
        async with self.app as client:
            for _ in range(5):
                response = await client.post('/')
                self.assertEqual(response.status_code, 200)

            # Simulate a GET request to retrieve the counter value
            response = await client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Counter: 5', await response.get_data())

if __name__ == '__main__':
    unittest.main()