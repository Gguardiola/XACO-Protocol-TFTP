from socket import *
print("##############################################")
print("#####                                    #####")
print("#####          UDP SERVER - PUT          #####")
print("#####          Alex P. y Gabriel         #####")
print("#####                v2.0                #####")
print("#####                                    #####")
print("##############################################")
# Default to listening on port 12000
serverPort = 12004
size = 1024

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
	#try:
	command = message.decode().split()
	#except UnicodeDecodeError:
	#	Este command necesitaria recibir el nuevo mensaje del cliente, enttonces tendriamos que modificar el cliente
	#	command = ""

	if len(command) > 0:

		if command[0].upper() == 'PUT':
			newSize, serverAddress = serverSocket.recvfrom(size)
			#print("SIZE " + newSize.decode())
			size = int(newSize.decode())
			print("[SERVIDOR]: Tamaño de paquetes establecido a {} bytes.".format(size))

			fileExistsChecker = True
			totalSize, serverAddress = serverSocket.recvfrom(size)
			totalSize = totalSize.decode()
			#si lo ha encontrado, recoge el tamaño del archivo para informar del estado de la descarga
			if "encontrado" in totalSize:
				totalSize = totalSize.split("|");totalSize = totalSize[1]

			else:
				fileExistsChecker = False

			if fileExistsChecker:
				#recibimos el primer paquete
				data, serverAddress = serverSocket.recvfrom(size)
				#DEBUG
				filename = "test2.txt"
				#filename = command[1]
				f = open(filename, "wb")
				packetsRecv = len(data)
				while( len(data) > 0):

					f.write(data)
					print("he escrito esto {}".format(len(data)))
					print("[SERVIDOR]:  Descargando [{}] {}/{} (bytes)".format(command[1],packetsRecv,totalSize))
					if len(data) == size:
						data, serverAddress = serverSocket.recvfrom(size)
						packetsRecv += len(data)
						print("EL SIGUIENTE DATA ES {}".format(len(data)))
					elif (len(data) < size):
						# PERO PARA CERRAR LA CONEXION
						print("start {}".format(len(data)))
						print("start SIZE {}".format(size))
						data, serverAddress = serverSocket.recvfrom(len(data))
						print("chivato {}".format(len(data)))
						#BYTE 0 PERO NO ES BYTE 0, QUIERO Q ME LO ENVIE AKIIIII
						print("[SERVIDOR]: {} DESCARGADO CON ÉXITO.".format(command[1]))
						#ESTO ES PARA QU PETE Y NO HAYA BUCLE
						#data, serverAddress = serverSocket.recvfrom(1)
						#if len(data) == 0:
			else:
				print("[SERVIDOR]: {} NO ENCONTRADO.".format(command[1]))	
			f.close()
