import socket
import random
connected = False
for i in range(100):
	print("Testing...")
	if random.random() > 0.95 and not connected:
		print("connecting")
		s = socket.socket()
		#s.settimeout(0)
		s.connect(("localhost", 10005))
		connected = True
