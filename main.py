import asyncio
import aiohttp


URL = "https://public.api.openprocurement.org/api/2.5/tenders/"


async def fetch(sem, session, url):
    file_name = url.split("/")[-1]
    async with sem, session.get(url) as response:
        with open(f"data/{file_name}.json", "wb") as out:
            async for chunk in response.content.iter_chunked(4096):
                out.write(chunk)


async def fetch_all(urls, loop):
    sem = asyncio.BoundedSemaphore(2)
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(
            *[fetch(sem, session, url) for url in urls]
        )
        return results


if __name__ == '__main__':
    with open("links.txt", "r") as ids_file:
        tenders = ids_file.read().splitlines()
    urls = [URL + tender_id for tender_id in tenders]
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(fetch_all(urls, loop))
    
