
from __future__ import division
import asyncio
import websockets
import json
import pyaudio
# from google.cloud.speech import enums
# from lomond import WebSocket, events

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
CHUNK = int(RATE / 1)

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)



# async def microphone_client():
#     websocket = WebSocket('ws://localhost:6000/transcribe')
#     # while True:
#     for event in websocket:
#         if event.name == 'poll':
#             data = stream.read(CHUNK)
#             websocket.send_binary(data)
#         if event.name == 'text':
#             print(event.text)


async def microphone_client():
    async with websockets.connect(
            'ws://34.105.32.194:6000/transcribe') as websocket:
        # await websocket.send(json.dumps({|
        #     "rate": RATE,
        #     "format": enums.RecognitionConfig.AudioEncoding.LINEAR16,
        #     "language": 'en-IN'
        # }))

        while True:
            data = stream.read(CHUNK)
            await websocket.send(data)



asyncio.get_event_loop().run_until_complete(microphone_client())