import unittest
from unittest.mock import patch, AsyncMock

import httpx

from src.utilities.request_helper import get_url, RetryableHttpError


class TestRequestHelper(unittest.IsolatedAsyncioTestCase):
    async def test_get_url(self):
        url = "https://www.google.com"
        response, status_code = await get_url(url)
        self.assertEqual(status_code, 200)
        self.assertIn("html", response)
    
    @patch('src.utilities.request_helper.httpx.AsyncClient.get', new_callable=AsyncMock)
    async def test_scrape_data_unavailable_website(self, mock_get):
        mock_get.return_value = httpx.Response(404, content=b'', request=mock_get)
        
        with self.assertRaises(RetryableHttpError) as context:
            await get_url("url")
        
        exception = context.exception
        print(exception)
        self.assertEqual(exception.status_code, mock_get.return_value.status_code)


if __name__ == "__main__":
    unittest.main()
