from socket import *
import os
print("##############################################")
print("#####                                    #####")
print("#####          UDP CLIENT - PUT          #####")
print("#####          Alex P. y Gabriel         #####")
print("#####                v1.0                #####")
print("#####                                    #####")
print("##############################################")


serverName = 'localhost'
serverPort = 12004
size = 1024
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
		
		clientSocket.sendto(client_msg.encode(),(serverName,serverPort))

		f = open(filename, "rb")
		data = f.read(size)
		packetsSended = len(data)
		totalSize = os.path.getsize(filename)
		while (len(data) > 0):
			percent = round(((packetsSended/int(totalSize))*100),2)
			if (clientSocket.sendto(data, (serverName, serverPort))):
				print("Enviando [{}] {}/{} (bytes) - {}%".format(filename,packetsSended,totalSize,percent))
					
				if(len(data) == size):
					data = f.read(size)
					packetsSended += len(data)
					if (len(data) == 0): # Si es un fichero multiplo de size enviamos un paquete con 0 bytes de datos para comunicar al cliente que hemos acabado
						print("{} ENVIADO CON EXITO A {}".format(filename,serverName))
						clientSocket.sendto(data, (serverName, serverPort))
				else:
					data = bytes()

		f.close()

except FileNotFoundError:
	print("[SERVIDOR]: No se encuentra el fichero en el servidor!.")
	clientSocket.sendto(bytes(), (serverName, serverPort))

clientSocket.close()

