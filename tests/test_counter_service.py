import unittest
import requests

class TestCounterService(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost/"

    def test_get_request(self):
        response = requests.get(self.url)
        
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.text.startswith("Counter: "))
        self.assertTrue(response.text[9:].isdigit())

    def test_post_request(self):
        response = requests.post(self.url)
        
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.text.startswith("Counter: "))
        self.assertTrue(response.text[9:].isdigit())

if __name__ == '__main__':
    unittest.main()
