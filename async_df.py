import random
import asyncio
import aiohttp
import pandas as pd


SLEEP_RANGE = 0.6, 0.7
CONCURRENT_CONNECTIONS = 5


async def fetch(sem, session, url):
    async with sem, session.get(url, raise_for_status=True) as response:
        await asyncio.sleep(random.uniform(*SLEEP_RANGE))
        data = await response.json()
        return {"tenderid": url.split("/")[-1], "data": data}


async def fetch_all(urls, loop):
    sem = asyncio.BoundedSemaphore(CONCURRENT_CONNECTIONS)
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(
            *[fetch(sem, session, url) for url in urls]
        )
        return pd.DataFrame(results)


if __name__ == '__main__':

    urls = (
        "https://public.api.openprocurement.org/api/2.5/tenders/6a0585fcfb05471796bb2b6a1d379f9b",
        "https://public.api.openprocurement.org/api/2.5/tenders/d1c74ec8bb9143d5b49e7ef32202f51c",
        "https://public.api.openprocurement.org/api/2.5/tenders/a3ec49c5b3e847fca2a1c215a2b69f8d",
        "https://public.api.openprocurement.org/api/2.5/tenders/52d8a15c55dd4f2ca9232f40c89bfa82",
        "https://public.api.openprocurement.org/api/2.5/tenders/b3af1cc6554440acbfe1d29103fe0c6a",
        "https://public.api.openprocurement.org/api/2.5/tenders/1d1c6560baac4a968f2c82c004a35c90",
    ) 

    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(fetch_all(urls, loop))
    print(data)
