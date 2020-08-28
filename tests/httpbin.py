import random
import logging
import asyncio
import aiohttp
from time import perf_counter 


URLS = ["http://httpbin.org/anything"] * 100
LIMIT = 5
SLEEP_RANGE = 0.3, 0.8


async def fetch(sem, session, url):
    async with sem, session.get(url, raise_for_status=True) as response:
        logging.info("Виконав запит")
        await asyncio.sleep(random.uniform(*SLEEP_RANGE))
        with open("data.json", "wb") as out:
            async for chunk in response.content.iter_chunked(4096):
                out.write(chunk)
        logging.info("Записав файл")

async def fetch_all(urls, loop):
    sem = asyncio.BoundedSemaphore(LIMIT)
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(
            *[fetch(sem, session, url) for url in urls]
        )
        return results


def make_requests(urls):
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(fetch_all(urls, loop)) 


if __name__ == '__main__':
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        handlers=[
            logging.FileHandler("test.log"),
            logging.StreamHandler()
        ]
    )
    
    start = perf_counter()
    make_requests(URLS)
    stop = perf_counter() 
    
    time, N = stop - start, len(URLS)
    per_s = N/time
    per_m = per_s * 60
    per_h = per_m * 60
    per_d = per_h * 24

    logging.info(
        f"N: {N}, total time: {time:.2f}; " +
        f"BoundedSemaphore({LIMIT}), sleep(random.uniform({SLEEP_RANGE})); " +
        f"{per_s:.2f}/1сек, {per_m:.2f}/1хв, {per_h:.2f}/1год, {per_d:.2f}/1доба"
    )
