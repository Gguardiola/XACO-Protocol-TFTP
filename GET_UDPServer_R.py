# Simple UDP based server that upper cases text
import sys
import time
import argparse

from socket import *

# Default to listening on port 12000
serverPort = 12000
size = 1024

# Setup IPv4 UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Specify the welcoming port of the server
serverSocket.bind(('', serverPort))

print ("El Servidor esta listo para recibir")
while True:
	message, clientAddress = serverSocket.recvfrom(size)
	client_msg = message.decode()
	
	print("Client connected {} -- ".format(clientAddress, client_msg), end='')
	command = client_msg.split()
	if len(command) > 0:
		if command[0] == 'get':
			print("GET /{}".format(command[1]))
			try:
				f = open(command[1], "rb")
				data = f.read(size)
				print(" enviando... %s" %len(data))
				while( len(data) > 0):
					if serverSockett.sendto(data, clientAddress):
						if len(data) == size:
							data = f.read(size)
							if len(data) == 0:
								serverSocket.sendto(data, clientAddress)
						else:
							data = bytes()
					print(" enviando... %s" %len(data))
			except IOError as e:
				print("File not found")
				serverSocket.sendto(bytes(), clientAddress)
				print(e)
			finally:
				try:
					f.close()
				except e:
					print(e)
	
	#serverSocket.sendto(modifiedMessage.encode(), clientAddress)
