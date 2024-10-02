import pyaudio
import wave
import pickle
import struct



CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
INPUT_INDEX=1


def get_input_device_id():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

def record():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,input_device_index=INPUT_INDEX)
    print('Recording...')
    obj = wave.open('output.wav', 'wb')
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(p.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    while True:
        try:
            frame = stream.read(CHUNK)
            """ a = pickle.dumps(frame)
            msg = struct.pack("Q",len(a))+a
            conn.sendall(msg) """
            obj.writeframes(bytes(frame))
        except KeyboardInterrupt:
            break
    stream.close()
    p.terminate()
    obj.close()

#get_input_device_id()

record()