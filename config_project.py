import pyaudio


#Audio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
INPUT_INDEX=1
OUTPUT_INDEX=3 

#connection
HOST = '192.168.56.1' # This is RaspberryPi IP address
APORT = 8081 # This is audio port
VPORT = PORT = 8080 #Intial connection port and video port is the same
