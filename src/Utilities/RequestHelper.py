import httpx


async def get_url(url):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text, response.status_code
    except httpx.RequestError as exception:
        print(f"Chyba při requestu: {exception}")
        return None
