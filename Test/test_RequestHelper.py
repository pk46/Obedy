import unittest
from src.Utilities.RequestHelper import get_url


class TestRequestHelper(unittest.IsolatedAsyncioTestCase):
    async def test_get_url(self):
        url = "https://www.google.com"
        response, status_code = await get_url(url)
        self.assertEqual(status_code, 200)


if __name__ == "__main__":
    unittest.main()
