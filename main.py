import argparse, logging, os.path, json, uvicorn
from fastapi import FastAPI, WebSocket, UploadFile, File

app = FastAPI()

@app.websocket("/transcribe")
async def recognize(ws: WebSocket):
    start_time = None
    gSem_acquired = False
    await ws.accept()
    while True:
        print('listening')



print('Running in the port: ' + str(6000) + '. Environment: ')
uvicorn.run(app, host="0.0.0.0", port=80)
