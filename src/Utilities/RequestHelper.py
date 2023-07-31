import httpx


class RetryableHttpError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code


async def get_url(url, max_retries=3):
    for retry in range(1, max_retries + 1):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.text, response.status_code
        except httpx.RequestError:
            print(f"Pokus č. {retry} selhal chybou RequestError")
        except httpx.HTTPStatusError as http_error:
            if 500 <= http_error.response.status_code < 600:
                print(f"Pokus č. {retry} selhal HTTP chybou: {http_error.response.status_code}")
            elif 400 <= http_error.response.status_code < 500:
                print(f"Pokus č. {retry} selhal HTTP chybou: {http_error.response.status_code}")
                if retry == max_retries:
                    raise RetryableHttpError(f"Pokus č. {retry} selhal HTTP chybou: {http_error}",
                                             http_error.response.status_code)
        except Exception as general_error:
            print(f"Pokus č. {retry} selhal obecnou chybou: {general_error}")
            if retry == max_retries:
                raise
            else:
                continue
