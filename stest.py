import socket


def server_program():
    # get the hostname
    host = '192.168.56.1'
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    while True:
        try:
            server_socket.listen(2)
            conn, address = server_socket.accept()  # accept new connection
            print("Connection from: " + str(address))
            while True:
                # receive data stream. it won't accept data packet greater than 1024 bytes
                data = conn.recv(1024).decode()
                if not data:
                    # if data is not received break
                    break
                print("from connected user: " + str(data))
                data = input(' -> ')
                conn.send(data.encode())  # send data to the client

        except Exception as e:
            print('disconnected')

#conn.close()  # close the connection

# This is server code to send video and audio frames over TCP

import socket
import threading, wave, pyaudio,pickle,struct

host_name = socket.gethostname()
host_ip = '85.23.95.56'#  socket.gethostbyname(host_name)
print(host_ip)
port = 9611

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
INPUT_INDEX=1

def audio_stream():
    server_socket = socket.socket()
    server_socket.bind((host_ip, (port-1)))

    server_socket.listen(5)
  
    
    p = pyaudio.PyAudio()
    print('server listening at',(host_ip, (port-1)))
   
    
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,put_device_index=INPUT_INDEX)


             

    client_socket,addr = server_socket.accept()
 
    data = None
    while True:
        if client_socket:
            while True:
                a = pickle.dumps(data)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
                
t1 = threading.Thread(target=audio_stream, args=())
t1.start()


""" 
if __name__ == '__main__':
    server_program() """