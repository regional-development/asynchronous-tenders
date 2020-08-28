import random
import logging
import asyncio
import aiohttp
from time import perf_counter 


URL = "https://public.api.openprocurement.org/api/2.5/tenders/"
LIMIT = 5
SLEEP_RANGE = 0.4, 1


async def fetch(sem, session, url):
    filename = url.split("/")[-1]
    async with sem, session.get(url) as response:
        # logging.info(f"зробив запит: {filename}")
        await asyncio.sleep(random.uniform(*SLEEP_RANGE))
        with open(f"data/{filename}.json", "wb") as out:
            async for chunk in response.content.iter_chunked(4096):
                out.write(chunk)


async def fetch_all(urls, loop):
    sem = asyncio.BoundedSemaphore(LIMIT)
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(
            *[fetch(sem, session, url) for url in urls]
        )
        return results


if __name__ == '__main__':
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        handlers=[
            logging.FileHandler("perf_counter.log"),
            logging.StreamHandler()
        ]
    )

    start = perf_counter()

    with open("links.txt", "r") as ids_file:
        tenders = ids_file.read().splitlines()
    urls = [URL + tender_id for tender_id in tenders]
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(fetch_all(urls, loop))
    
    stop = perf_counter() 

    time, N = stop - start, len(urls)
    logging.info(
        f"N: {N}, total time: {time:.2f}; {N/time:.2f}/1сек" 
    )
