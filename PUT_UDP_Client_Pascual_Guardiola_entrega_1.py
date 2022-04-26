from pickle import TRUE
from socket import *
import os
print("##############################################")
print("#####                                    #####")
print("#####          UDP CLIENT - PUT          #####")
print("#####          Alex P. y Gabriel         #####")
print("#####                v2.0                #####")
print("#####                                    #####")
print("##############################################")


serverName = 'localhost'
serverPort = 12004
size = 1024
packetSizeOpt = [32,64,128,256,512,1024,2048]
# Request IPv4 and UDP communication
clientSocket = socket(AF_INET, SOCK_DGRAM)

method = "PUT"
# Read in some text from the user
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


	if method.upper() == 'PUT':
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
		size = int(newSize)
		#envia el tamaño del paquete
		clientSocket.sendto(newSize.encode(),(serverName,serverPort))
		print("Tamaño del paquete establecido en " + newSize + " bytes.")	
		
		f = open(filename, "rb")
		data = f.read(size)
		packetsSended = len(data)
		totalSize = os.path.getsize(filename)

		clientSocket.sendto("encontrado |{}".format(totalSize).encode(),(serverName,serverPort))
		
		while True:
			percent = round(((packetsSended/int(totalSize))*100),2)
			if (clientSocket.sendto(data, (serverName, serverPort))):
				
				print("Enviando [{}] {}/{} (bytes) - {}%".format(filename,packetsSended,totalSize,percent))
				if(len(data) == size):
					data = f.read(size)
					packetsSended += len(data)
				if(len(data) == 0):
					print("{} ENVIADO CON EXITO A {}".format(filename,serverName))
					clientSocket.sendto(bytes(), (serverName, serverPort))
					break
				elif(len(data) < size): # Si es un fichero multiplo de size enviamos un paquete con 0 bytes de datos para comunicar al cliente que hemos acabado
					clientSocket.sendto(data, (serverName, serverPort))
					data = f.read(size)
					packetsSended += len(data)
					percent = round(((packetsSended/int(totalSize))*100),2)
					print("Enviando [{}] {}/{} (bytes) - {}%".format(filename,packetsSended,totalSize,percent))
					print("{} ENVIADO CON EXITO A {}".format(filename,serverName))
					clientSocket.sendto(bytes(), (serverName, serverPort))
					break
		f.close()

except FileNotFoundError:
	print("[SERVIDOR]: No se encuentra el fichero en el servidor!.")
	clientSocket.sendto(bytes(), (serverName, serverPort))

clientSocket.close() #ILEGAL putada de las gordas

