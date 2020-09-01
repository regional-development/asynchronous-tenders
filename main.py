import os
import random
import logging
import asyncio
import aiohttp
import pandas as pd
from time import perf_counter 


LIMIT = 5
SLEEP_RANGE = 0.4, 0.8
SAMPLE_SIZE = 100_000


async def fetch(sem, session, url):
    filename = url.split("/")[-1]
    async with sem, session.get(url, raise_for_status=True) as response:
        await asyncio.sleep(random.uniform(*SLEEP_RANGE))
        with open(f"data/{filename}.json", "wb") as out:
            async for chunck in response.content.iter_chunked(4096):
                out.write(chunck)


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

    logging.info("Починаю виконувати скрипт")

    already_downloaded = [f.split(".")[0] for f in os.listdir("data")]
    df = pd.read_csv("./links_ok.csv")
    sample = df.loc[df["status"].eq(0)].sample(SAMPLE_SIZE)["tender_id"]

    logging.info("Починаю виконувати запити")
    start = perf_counter()
    loop = asyncio.get_event_loop()
    try:
        data = loop.run_until_complete(fetch_all(sample, loop))
        logging.info("Виконав усі запити")
    except (
        KeyboardInterrupt,
        aiohttp.ClientConnectionError,
        aiohttp.client_exceptions.ClientResponseError
        ) as e:
        logging.exception("Сталася помилка")
        loop.stop()
        logging.info("Зупинив event loop")
    stop = perf_counter()

    df["tenders"] = df["tender_id"].str.split("/").str[-1]
    downloaded = [f.split(".")[0] for f in os.listdir("data")]
    df.loc[df["tenders"].isin(downloaded), "status"] = 1
    df.drop("tenders", 1).to_csv("./links_ok.csv")

    time, N = stop - start, len(downloaded) - len(already_downloaded) 
    logging.info(
        f"Завантажив {N} тендерів за {time:.2f}s; {N/time:.2f}/1сек" 
    )
    logging.info("Закінчив виконувати скрипт \n")