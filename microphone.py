import pyaudio
import wave
import pickle
import struct



CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5


def get_input_device_id():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

def record(stop, conn):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
    print('Recording...')

    while not stop:
        try:
            frame = stream.read(CHUNK)
            a = pickle.dumps(frame)
            msg = struct.pack("Q",len(a))+a
            conn.sendall(msg)
        except KeyboardInterrupt:
            break
    stream.close()
    p.terminate()

