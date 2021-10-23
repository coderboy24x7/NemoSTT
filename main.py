import argparse, logging, os.path, json, uvicorn
from fastapi import FastAPI, WebSocket, UploadFile, File

app = FastAPI()

@app.websocket("/transcribe")
async def recognize(ws: WebSocket):
    start_time = None
    gSem_acquired = False
    await ws.accept()
    while True:
        data = await ws.receive()
        data = data['text'] if 'text' in data else data
        data = data['bytes'] if 'bytes' in data else data
        data = bytearray(data) if isinstance(data, bytes) else data
        if isinstance(data, bytearray):
            if not start_time:
                start_time = time()
                stream = engine.stream()
                assert not gSem_acquired
                gSem.acquire(blocking=True)
                gSem_acquired = True
            stream.feedAudioContent(np.frombuffer(data, np.int16))
        elif isinstance(data, str) and data == 'EOS':
            eos_time = time()
            text = stream.finishStream()
            logger_Deepspeech.info("Recognized:" + text)
            await ws.send_text(text)
            gSem.release()
            gSem_acquired = False
            start_time = None
        else:
            if gSem_acquired:
                gSem.release()
                gSem_acquired = False
            break


@app.websocket('/')
async def healthcheck(ws: WebSocket):
    await ws.accept()
    """Route for simple healthcheck that simply returns greeting message"""
    await ws.send_json({
        "api": 'Vozy STT',
        "status": "200"
    })



print('Running in the port: ' + str(6000) + '. Environment: ')
uvicorn.run(app, host="0.0.0.0", port=6000)
