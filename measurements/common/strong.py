import socket
import time
import threading

IP = "10.0.0.2"
PORT = 12345
MESSAGE = b"A" * 10 #10 bytes

# function to send data in a thread
def send_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        sock.sendto(MESSAGE, (IP, PORT))
       # time.sleep(0.0001) #sleep for 100 us before sending the next packet

# create and start threads
for i in range(100):
    t = threading.Thread(target=send_data)
    t.start()
