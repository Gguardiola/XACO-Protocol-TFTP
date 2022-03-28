# Simple UDP based server that upper cases text

from socket import *

# Default to listening on port 12000
serverPort = 12000
size = 512

# Setup IPv4 UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Specify the welcoming port of the server
serverSocket.bind(('', serverPort))

print ("El Servidor esta listo para recibir")
while True:
	message, clientAddress = serverSocket.recvfrom(size)
	archive = message.decode()
	
	print("Client connected {} -- ".format(clientAddress, message), end='')
	command = message.split()
	if len(command) > 0:
		if command[0] == 'put':
			if len(command) == 2:
				print("PUT {}".format(command[1]))
				desti = command[1]
			if len(command) == 3:
				print("PUT {}".format(command[1], command[2]))
				desti = command[2]
			archive, serverAddress = serverSocket.recvfrom(size)
			print(" recibiendo... %s" %len(data))
			try:
				f = open(desti, "wb")
				while(archive > 0):
					f.write(archive)
					if len(archive) == size:
						archive, serverAddress = serverSocket.recvfrom(size)
					else:
						archive = bytes()
					print(" recibiendo... %s" %len(data))
			except timeout:
				print("timeout")
			except IOError:
				print("File requested not found")
			finally:
				try:
					f.close()
				except:
					pass	
print("He copiado con exito")
	#serverSocket.sendto(modifiedMessage.encode(), clientAddress)
