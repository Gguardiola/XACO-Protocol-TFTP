
from socket import *


print("##############################################")
print("#####                                    #####")
print("#####          UDP CLIENT - GET          #####")
print("#####          Alex P. y Gabriel         #####")
print("#####                v2.0                #####")
print("#####                                    #####")
print("##############################################")


# Default to running on localhost, port 12000
serverName = 'localhost'
serverPort = 12004
packetSize = 1024
packetSizeOpt = [32,64,128,256,512,1024,2048]
method = "GET"
# Request IPv4 and UDP communication

clientSocket = socket(AF_INET, SOCK_DGRAM)

try:
	while True:
		filename = input("Nombre del archivo: ")
		if len(filename) == 0:
			print("ERROR - INTRODUCE UN ARCHIVO.")
		else:
			msgLength = filename.split(" ")

			if len(msgLength) > 1:
				print("ERROR - INTRODUCE SOLO UN ARCHIVO.")
			else:
				break

	client_msg = method + " " + filename

	if method.upper() == 'GET':
		#establecer el tamaño del paquete
		newSize = 0
		while newSize not in packetSizeOpt:
			try:
				newSize = int(input("Tamaño del paquete: "))
				if newSize not in packetSizeOpt:
					print("ERROR - Introduce un valor entre 32 y 2048.")
			except AttributeError:
				print("ERROR - Introduce un valor numerico.")
	
		#enviamos el comando con el fichero que vamos a subir
		clientSocket.sendto(client_msg.encode(),(serverName,serverPort))

		newSize = str(newSize)
		packetSize = int(newSize)
		#envia el tamaño del paquete
		clientSocket.sendto(newSize.encode(),(serverName,serverPort))
		print("Tamaño del paquete establecido en " + newSize + " bytes.")

		fileExistsChecker = True
		totalSize, serverAddress = clientSocket.recvfrom(packetSize)
		totalSize = totalSize.decode()
		#si lo ha encontrado, recoge el tamaño del archivo para informar del estado de la descarga
		if "encontrado" in totalSize:
			totalSize = totalSize.split("|");totalSize = totalSize[1]

		else:
			fileExistsChecker = False	

		if fileExistsChecker:
			#recibimos el primer paquete		
			data, serverAddress = clientSocket.recvfrom(packetSize)

			#DEBUG
			filename = "test.txt"
			f = open(filename, "wb")
			packetsRecv = len(data)
			while len(data) > 0:
				f.write(data)
				print("Descargando [{}] {}/{} (bytes)".format(filename,packetsRecv,totalSize))
				data, serverAddress = clientSocket.recvfrom(packetSize)
				packetsRecv += len(data)							
			print("{} DESCARGADO CON ÉXITO.".format(filename))	
			f.close()	
			clientSocket.close()
	else:
		print("ERROR - Método no soportado")
		clientSocket.close()

except ConnectionResetError as e:
	print(e, "El servidor no está disponible")
	clientSocket.close()

except ConnectionRefusedError as e:
	print(e, "El servidor no está disponible")
	clientSocket.close()
except TimeoutError as e:
	print(e, "El servidor no está disponible")
	clientSocket.close()



