from time import sleep
import asyncio

async def HolaMundo():
    print("comienzo")
    await asyncio.sleep(2)
    print("acabo")

asyncio.run(HolaMundo())