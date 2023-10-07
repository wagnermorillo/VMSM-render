from asgiref.sync import sync_to_async
import time
#####################################
# await sync_to_async(asyncro, thread_sensitive=True)()


# task1 = asyncio.ensure_future(function1)
# task2 = asyncio.ensure_future(function2)
# await asyncio.wait([task1, task2])


# await asyncio.gather(function1(), function2())
#####################################

@sync_to_async
def asyncro():
    print("preparando el async")
    time.sleep(5)
    print("finalizado")
    return "hola mundo"


