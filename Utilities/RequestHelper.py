import httpx


async def get_url(url, max_retries=4):
    for retry in range(1, max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.text
        except Exception as http_error:
            print(f"Pokus č. {retry} selhal chybou: {http_error}")
            if retry == max_retries:
                return http_error
