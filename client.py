# lets make the client code
import socket,cv2, pickle,struct, pyaudio, threading
from playsound import playsound


# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '85.23.95.56' # paste your server ip address here
port = 8080
client_socket.connect((host_ip,port)) # a tuple
print('Connected to server', host_ip, '+ ', port)


#-----------------------------
# Audio innit
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
OUTPUT_INDEX=5

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK, output_device_index=OUTPUT_INDEX)
#-----------------------------


def camera_stream():
	data = b""
	payload_size = struct.calcsize("Q")
	while True:
		if client_socket:
			while len(data) < payload_size:
				packet = client_socket.recv(4*1024) # 4K
				if not packet: break
				data+=packet
			packed_msg_size = data[:payload_size]
			data = data[payload_size:]
			msg_size = struct.unpack("Q",packed_msg_size)[0]
			
			while len(data) < msg_size:
				data += client_socket.recv(4*1024)
			try:
				frame_data = data[:msg_size]
				data  = data[msg_size:]
				frame = pickle.loads(frame_data)
				cv2.imshow("RECEIVING VIDEO",frame)
				key = cv2.waitKey(1) & 0xFF
				if key == ord('q'):
					cv2.destroyAllWindows()
					break
			except Exception as e:
				cv2.destroyAllWindows()
				break
		else:
			pass


def audio_stream():

	s=socket.socket()
	s.connect((host_ip,port-1))
	print('Audio stream connected to server', host_ip, '+ ', port-1)

	""" data = b""
	payload_size = struct.calcsize("Q") """


	while True:
		if s:
			""" while len(data) < payload_size:
				packet = s.recv(4*1024) # 4K
				if not packet: break
				data+=packet
			packed_msg_size = data[:payload_size]
			data = data[payload_size:]
			msg_size = struct.unpack("Q",packed_msg_size)[0]
			
			while len(data) < msg_size:
				data += client_socket.recv(4*1024) 
 			try:
				frame_data = data[:msg_size]
				data  = data[msg_size:]
				frame = pickle.loads(frame_data) """
			
			try:
				frame = s.recv(CHUNK)
				stream.write(frame)
			except KeyboardInterrupt:
				cv2.destroyAllWindows()
				stream.close()
				break
			except Exception as e:
				cv2.destroyAllWindows()
				stream.close()
				break
		else:
			pass



#client_socket.close()
tf = threading.Thread(target=camera_stream)
ta = threading.Thread(target=audio_stream)

tf.start()
ta.start()