import socket

IP = "10.0.0.2"
PORT = 12345
MESSAGE = b"A" * (1024*1024*100) #100MB

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

chunk_size = 8192
offset = 0

while True:
    offset = 0
    while offset < len(MESSAGE):
        sent = sock.sendto(MESSAGE[offset:offset+chunk_size], (IP, PORT))
        offset += sent
