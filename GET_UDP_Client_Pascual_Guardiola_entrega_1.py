
from socket import *


print("##############################################")
print("#####                                    #####")
print("#####          UDP CLIENT - GET          #####")
print("#####          Alex P. y Gabriel         #####")
print("#####                v1.0                #####")
print("#####                                    #####")
print("##############################################")


# Default to running on localhost, port 12000
serverName = 'localhost'
serverPort = 12004
packetSize = 1024
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

		#enviamos el comando con el fichero que vamos a subir
		clientSocket.sendto(client_msg.encode(),(serverName,serverPort))

		data, serverAddress = clientSocket.recvfrom(packetSize)

		#DEBUG
		#filename = "test.txt"
		f = open(filename, "wb")
		packetsRecv = len(data)
		while len(data) > 0:
			f.write(data)
			if len(data) == packetSize:
				data, serverAddress = clientSocket.recvfrom(packetSize)
				packetsRecv += len(data)
				print("Descargando [{}] {} (bytes)".format(filename,packetsRecv))			
			else:
				print("{} DESCARGADO CON ÉXITO.".format(filename))
				data = bytes()
				


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



