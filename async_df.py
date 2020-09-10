import random
import asyncio
import aiohttp
import pandas as pd
from pathlib import Path
from datetime import datetime


PATH = Path(__file__).resolve().parent
INPUTS = PATH / "sample.csv"
OUTPUTS = PATH / "output_table.csv"
SLEEP_RANGE = 0.6, 0.7
CONCURRENT_CONNECTIONS = 5


async def fetch(sem, session, url):
    async with sem, session.get(url) as response:
        await asyncio.sleep(random.uniform(*SLEEP_RANGE))
        data = await response.json()
        return {
            "ProzorroTenderID": url.split("/")[-1], 
            "JSON_Value": data.get("data", "error"),
            "DateInserted": pd.to_datetime(datetime.now()),
        } 


async def fetch_all(urls, loop):
    sem = asyncio.BoundedSemaphore(CONCURRENT_CONNECTIONS)
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(
            *[fetch(sem, session, url) for url in urls]
        )
        df = pd.DataFrame(results)
        return df.loc[df["JSON_Value"].ne("error")]


def read_tenders():
    df = pd.read_csv(INPUTS, sep='\t', header=None)
    df.columns = ["ProzorroTenderID"]
    df["ProzorroTenderID"] = (
        "https://public.api.openprocurement.org/api/2.5/tenders/" + 
        df["ProzorroTenderID"]
    )
    return df["ProzorroTenderID"].tolist()


if __name__ == '__main__':
    
    urls = read_tenders()
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(fetch_all(urls, loop))
    print(data)
    data.to_csv(OUTPUTS, index=False)
