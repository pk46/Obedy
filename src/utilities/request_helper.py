import httpx
import logging


class RetryableHttpError(Exception):
    
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code


logging.basicConfig(level=logging.INFO)  # comment this line to create log file otherwise it will log into the console


async def get_url(url, class_name=None):
    max_retries = 5
    for retry in range(1, max_retries + 1):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.text, response.status_code
        except httpx.RequestError:
            logging.error(f"{class_name}: pokus č. {retry} selhal chybou RequestError")
            if retry == max_retries:
                raise RetryableHttpError("", "RequestError")
        except httpx.HTTPStatusError as http_error:
            if 500 <= http_error.response.status_code < 600:
                logging.error(f"{class_name}: pokus č. {retry} selhal kvůli chybě {http_error.response.status_code}")
                if retry == max_retries:
                    raise RetryableHttpError("", http_error)
            elif 400 <= http_error.response.status_code < 500:
                logging.error(f"{class_name} pokus č. {retry} kvůli chybě {http_error.response.status_code}")
                if retry == max_retries:
                    raise RetryableHttpError("", http_error.response.status_code)
        except Exception as error:
            logging.error(f"{class_name} pokus č. {retry} selhal chybou: {error}")
            if retry == max_retries:
                raise RetryableHttpError("", error)
