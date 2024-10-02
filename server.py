
# This code is for the server sss
import socket, cv2, pickle,struct, pyaudio, threading
from time import sleep
import btn
import microphone

#-------------------------------------------------
# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '85.23.95.56'
print('HOST IP:',host_ip)
port = 8080
socket_address = (host_ip,port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:",socket_address)

# Socket Accept
client_socket,addr = server_socket.accept()
print('GOT CONNECTION FROM:',addr)
#-----------------------------------------------------
#Audio innit

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
INPUT_INDEX = 1

#----------------------------------------------------


def footage_stream(conn):
	client_socket=conn
	while True:

		try:
			""" if not client_socket_cam:
				server_socket.listen(5)
				client_socket_cam,addr = server_socket.accept() """
			if btn.btn_pressed():
				while True:
					if client_socket:
						vid = cv2.VideoCapture(0)
						vid.set(cv2.CAP_PROP_FPS, 60)
						while(vid.isOpened()):
							img,frame = vid.read()
							#frame = imutils.resize(frame,width=500)
							cv2.imshow('TRANSMITTING VIDEO',frame)
							a = pickle.dumps(frame)
							message = struct.pack("Q",len(a))+a
							client_socket.sendall(message)
							
							key = cv2.waitKey(1) & 0xFF
							if key ==ord('q') or btn.btn_pressed():
								print('?')
								cv2.destroyAllWindows()
								vid.release()
								break
					break
			else:
				pass
		except Exception as e:
			print('Disconected!')
			print(e)
			server_socket.listen(5)
			client_socket,addr = server_socket.accept()
			

def audio_stream():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((host_ip, port-1))
	s.listen(5)
	client_socket, addr=s.accept()
	print('Server for audio is connected at IP: ', host_ip, 'and Port: ', port-1)
	while True:
		try:
			while True:
				if btn.btn_pressed():
					while True:
						if client_socket:
							p = pyaudio.PyAudio()
							stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer= CHUNK,input_device_index=INPUT_INDEX)
							print('Recording...')
							while True:
								frame = stream.read(CHUNK)
								""" a = pickle.dumps(frame)
								msg = struct.pack("Q",len(a))+a
								client_socket.sendall(msg) """
								client_socket.send(frame)
								if btn.btn_pressed():
									stream.close()
									p.terminate()
									break
						break
				else:
					pass
		except Exception as e:
			print(e)
			print('Disconnected!!')

def change_start_exit_event_state():
	global start_exit_event
	start_exit_event = False
	while True:
		if btn.btn_pressed():
			start_exit_event = True
			sleep(5)
			start_exit_event = False
		else:
			pass


t1st=threading.Thread(target=change_start_exit_event_state)
t1st.start()
tf=threading.Thread(target=footage_stream, args=(client_socket,))

ta=threading.Thread(target=audio_stream)
ta.start()