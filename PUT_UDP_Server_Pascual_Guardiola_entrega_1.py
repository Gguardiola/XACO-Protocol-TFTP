from socket import *
print("##############################################")
print("#####                                    #####")
print("#####          UDP SERVER - PUT          #####")
print("#####          Alex P. y Gabriel         #####")
print("#####                v1.0                #####")
print("#####                                    #####")
print("##############################################")
# Default to listening on port 12000
serverPort = 12004
size = 1024
# https://prod.liveshare.vsengsaas.visualstudio.com/join?971C345B9ABA4B05CFD33C1C3A0E83F059E0
# Setup IPv4 UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

try:
	serverSocket.bind(('', serverPort))
except OSError:
	serverPort += 1
	serverSocket.bind(('', serverPort))
	print("[SERVIDOR]: Puerto en uso. Cambiando al {}".format(serverPort))

while True:
	print ("LISTO - El servidor está esperando por el puerto {}".format(serverPort))
	message, clientAddress = serverSocket.recvfrom(size)

	print("CONEXIÓN ESTABLECIDA - Client IP {}".format(clientAddress))
	command = message.decode().split()
	if len(command) > 0:
		if command[0].upper() == 'PUT':

			data, serverAddress = serverSocket.recvfrom(size)
			#DEBUG
			#filename = "test2.txt"
			filename = command[1]
			f = open(filename, "wb")
			packetsRecv = len(data)
			while( len(data) > 0):

				f.write(data)
				print("[SERVIDOR]:  Descargando [{}] {} (bytes)".format(command[1],packetsRecv))	
				if len(data) == size:
					data, serverAddress = serverSocket.recvfrom(size)
					packetsRecv += len(data)				
				else:
					print("[SERVIDOR]: {} DESCARGADO CON ÉXITO.".format(command[1]))
					data = bytes()

			f.close()
