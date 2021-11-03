import websockets, asyncio

async def Forward(message):
        url = 'ws://34.72.57.30:6000'
        async with websockets.connect(url) as websocket:
                await websocket.send(message)
def xmit_Loop(message):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(Forward(message))