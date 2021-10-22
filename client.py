from lomond import WebSocket, events



def websocket_runner(websocket):
    """blocks"""

    def on_event(event):
        if isinstance(event, events.Ready):
            global ready
            if not ready:
                print("Connected!")
            ready = True
        elif isinstance(event, events.Text):
            if 1: print(event.text)
        elif 1:
            # logging.debug(event)
            print('aaaa')

    for event in websocket:
        try:
            on_event(event)
        except:
            print('error handling %r', event)
            websocket.close()

websocket = WebSocket('ws://35.184.187.206:8891/transcribe')
# TODO: compress?
print("Connecting to '%s'..." % websocket.url)

websocket_runner(websocket)