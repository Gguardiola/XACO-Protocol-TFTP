from socket import *
import os
print("##############################################")
print("#####                                    #####")
print("#####          UDP SERVER - GET          #####")
print("#####          Alex P. y Gabriel         #####")
print("#####                v1.0                #####")
print("#####                                    #####")
print("##############################################")




# Default to listening on port 12000
serverPort = 12004
size = 1024

# Setup IPv4 UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Specify the welcoming port of the server
try:
	serverSocket.bind(('', serverPort))
except OSError:
	serverPort += 1
	serverSocket.bind(('', serverPort))
	print("[SERVIDOR]: Puerto en uso. Cambiando al {}".format(serverPort))

print ("LISTO - El servidor listo para recibir por el puerto {}".format(serverPort))
while True:
	message, clientAddress = serverSocket.recvfrom(size)
	client_msg = message.decode()
	
	print("CONEXIÓN ESTABLECIDA - Client IP {}".format(clientAddress))
	command = client_msg.split()
	if len(command) > 0:
		if command[0].upper() == 'GET':
			
			try:
				f = open(command[1], "rb")
				newSize, serverAddress = serverSocket.recvfrom(size)
				size = int(newSize.decode())
				print("[SERVIDOR]: Tamaño de paquetes establecido a {} bytes.".format(size))
						
				data = f.read(size)
				packetsSended = len(data)
				totalSize = os.path.getsize(command[1])
				
				while( len(data) > 0):
					percent = round(((packetsSended/int(totalSize))*100),2)
					if serverSocket.sendto(data, clientAddress):
						print("[SERVIDOR]: Enviando [{}] {}/{} (bytes) - {}%".format(command[1],packetsSended,totalSize,percent))
					
						if len(data) == size:
							data = f.read(size)
							packetsSended += len(data)
							if len(data) == 0:
								print("[SERVIDOR]: {} ENVIADO CON EXITO A {}".format(command[1],clientAddress))
								serverSocket.sendto(data, clientAddress)
						else:
							data = bytes()
					
			except FileNotFoundError:
				print("[SERVIDOR]: No se encuentra el fichero en el servidor!.")
				serverSocket.sendto(bytes(), clientAddress)

			f.close()
