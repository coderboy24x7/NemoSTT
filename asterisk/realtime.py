# Standard Python modules
from time import sleep

# Import everything from the audiosocket module
from audiosocket import *

# Create a new Audiosocket instance, passing it binding
# information in a tuple just as you would a standard Python socket
audiosocket = Audiosocket(("127.0.0.1", 1121))

# This assumes Audiosocket is being used via the Asterisk Dial() application
# and that the channel bridged with Audiosocket is using the U-Law audio codec.
# If the audio sounds courrupted, try commenting this out
audiosocket.prepare_output(rate=8000, ulaw2lin=True)

# This will block until a connection is received, returning
# a connection object when one occurs
conn = audiosocket.listen()


print('Received connection from {0}'.format(conn.peer_addr))


# While a connection exists, send all
# received audio back to Asterisk (creates an echo)
from scipy.io.wavfile import write
import numpy

audio = []
while conn.connected:
  audio_data = conn.read()
  conn.write(audio_data)
  print(audio_data)
  # audio.append(audio_data)
# for chunk in range(0, len(audio)):
#   # numpy.frombuffer(chunk, dtype=numpy.int16)
#   write(f'test{chunk}.wav', 16000,  numpy.frombuffer(audio[chunk], dtype=numpy.int16))

print('Connection with {0} over'.format(conn.peer_addr))