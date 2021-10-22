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
