import random
import logging
import asyncio
import aiohttp
import pandas as pd
from pathlib import Path
from time import perf_counter 


PATH = Path(__file__).resolve().parent
DATA = PATH / "data"

LIMIT = 5
SLEEP_RANGE = 0.4, 0.8
SAMPLE_SIZE = 150_000


async def fetch(sem, session, url):
    filename = url.split("/")[-1]
    async with sem, session.get(url, raise_for_status=True) as response:
        await asyncio.sleep(random.uniform(*SLEEP_RANGE))
        with open(DATA / f"{filename}.json", "wb") as out:
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
            logging.FileHandler(PATH / "perf_counter.log"),
            logging.StreamHandler()
        ]
    )

    logging.info("Починаю виконувати скрипт")

    already_downloaded = [f.parts[-1].split(".")[0] for f in DATA.rglob("*.json")]
    df = pd.read_csv(PATH / "links.csv")
    sample = df.loc[df["status"].eq(0)].sample(SAMPLE_SIZE)["tender_id"]

    logging.info("Починаю виконувати запити")
    start = perf_counter()
    loop = asyncio.get_event_loop()
    try:
        data = loop.run_until_complete(fetch_all(sample, loop))
        logging.info("Виконав усі запити")
    except:
        logging.exception("Сталася помилка")
        loop.stop()
        logging.info("Зупинив event loop")
    stop = perf_counter()

    df["tenders"] = df["tender_id"].str.split("/").str[-1]
    downloaded = [f.parts[-1].split(".")[0] for f in DATA.rglob("*.json")]
    df.loc[df["tenders"].isin(downloaded), "status"] = 1
    df.drop("tenders", 1).to_csv(PATH / "links.csv")

    time, N = stop - start, len(downloaded) - len(already_downloaded) 
    logging.info(
        f"Завантажив {N} тендерів за {time:.2f}s; {N/time:.2f}/1сек" 
    )
    logging.info("Закінчив виконувати скрипт \n")
