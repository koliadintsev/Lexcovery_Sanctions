from Search import elasticsearch_handler
import asyncio


async def test():
    r = await elasticsearch_handler.search_fuzzy_request("Roman Abramovich")
    print("a")

test()




