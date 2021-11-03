import asyncio
import websockets
import pyaudio
import socket
import time
import ssl
from audiosocket import *

nombre_cliente = socket.gethostname()
ip_cliente=socket.gethostbyname(nombre_cliente)


audiosocket = Audiosocket(("34.105.32.194", 1121))
call_conn = audiosocket.listen()
#audiosocket.prepare_output(rate=16000, channels=1)
print('Listening for Audiosocket connections')

async def microfono():
    """
    #instanciar pyaudio
    audio=pyaudio.PyAudio()
    #elegir el microfono adecuado
    inpu_devices=[]
    for i in range(audio.get_device_count()):
        dev = audio.get_device_info_by_index(i)
        if dev.get('maxInputChannels'):
            inpu_devices.append(i)
            print(i, dev.get('name'))
    if len(inpu_devices):
        dev_idx=-2
        while dev_idx not in inpu_devices:
            print('elija el dispositivo de entrada adecuado ')
            dev_idx = int(input())

    #open stream para grabar o reproducir audios
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=dev_idx,
                        frames_per_buffer=CHUNK)

    stream.start_stream()
    """
    empty_counter=0
    offset=10
    print(f'[INFO] Enviando streaming a VOZY-Server')
    #async with websockets.connect(
     #   'ws://localhost:2000') as websocket:
    async with websockets.connect(
            'ws://34.72.57.30:6000/transcribe') as websocket:
        while call_conn.connected:
        #while True:
            try:

                                
                #print(data)
                content = [call_conn.read()]
                print(audio_data for audio_data in content) 
                await websocket.send(audio_data for audio_data in content)
                text = await asyncio.wait_for(websocket.recv(), timeout=5)
                #print(text + ' ', end='')
                if len(text):
                    print(text, end=' ')
                    empty_counter = offset
                elif empty_counter > 0:
                    #print('\nTiempo restante', empty_counter)
                    empty_counter -= 1
                    if empty_counter == 0:
                        print('\n[INFO] conexión cerrada, transcurrierón mas de 3 segundos sin hablar...')
                        break
            except websockets.exceptions.ConnectionClosedError:
                #stream.stop_stream()
                #stream.close()
                #audio.terminate()
                print('[INFO] Transcripción concluida ...')
                break
            except OSError:
                #stream.stop_stream()
                #stream.close()
                #audio.terminate()
                print('[INFO] streaming closed')
                break

asyncio.get_event_loop().run_until_complete(microfono())
