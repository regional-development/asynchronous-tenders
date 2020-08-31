import random
import logging
import asyncio
import aiohttp
import pandas as pd
from time import perf_counter 


URL = "https://public.api.openprocurement.org/api/2.5/tenders/"
LIMIT = 5
SLEEP_RANGE = 0.4, 0.8
SAMPLE_SIZE = 150_000


async def fetch(sem, session, url):
    filename = url.split("/")[-1]
    try:
        async with sem, session.get(url, raise_for_status=True) as response:
            await asyncio.sleep(random.uniform(*SLEEP_RANGE))
            with open(f"data/{filename}.json", "wb") as out:
                async for chunck in response.content.iter_chunked(4096):
                    out.write(chunck)
    except aiohttp.client_exceptions.ClientResponseError as exc:
        logging.info(f"Помилка: {exc} для {filename}")
        await asyncio.sleep(60)


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

    df = pd.read_csv("./links_ok.csv")
    sample = df.loc[df["status"].eq(0)].sample(SAMPLE_SIZE)["tender_id"]
    
    start = perf_counter()
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(fetch_all(sample, loop))
    stop = perf_counter()

    df.loc[df["tender_id"].isin(sample), "status"] = 1
    df.to_csv("./links_ok.csv", index=False)

    time = stop - start 
    logging.info(
        f"N: {SAMPLE_SIZE}, total time: {time:.2f}; {SAMPLE_SIZE/time:.2f}/1сек" 
    )
