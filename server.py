
# This code is for the server 

import socket, cv2, pickle,struct,imutils
import btn
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
while True:
	if btn.btn_pressed():
		while True:
			if client_socket:
				vid = cv2.VideoCapture(0)
				
				while(vid.isOpened()):
					img,frame = vid.read()
					#frame = imutils.resize(frame,width=500)
					a = pickle.dumps(frame)
					message = struct.pack("Q",len(a))+a
					client_socket.sendall(message)
					
					cv2.imshow('TRANSMITTING VIDEO',frame)
					key = cv2.waitKey(1) & 0xFF
					if key ==ord('q'):
						client_socket.close()
						server_socket.close()
	else:
		pass