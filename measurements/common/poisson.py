import socket
import time
import termios
import sys
import select
import random
from math import exp

IP = "10.0.0.2"
PORT = 12345
MESSAGE = b"A" * 1000 #1000 bytes

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print ("WELCOME!!! PRESS THE r KEY TO REDUCE THE WAITING TIME BY A FACTOR 0.75")
reduction_factor=0.75
time.sleep(5)
print ("Current frequency is 10Hz")

def message_sending():
  lambd=0.1
  while True:
    for i in range(1000):
      sock.sendto(MESSAGE, (IP, PORT))
      #print(i)
      if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline()
            if line[0] == 'r':
                lambd = lambd * reduction_factor
                print ("New frequency is ", 1/lambd, "Hz")
      time.sleep(random.expovariate(1/lambd)) #sleep for a mean of lambd seconds before sending the next packet (Poisson distribution)

termios.tcflush(sys.stdin, termios.TCIFLUSH)
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))

message_sending()
