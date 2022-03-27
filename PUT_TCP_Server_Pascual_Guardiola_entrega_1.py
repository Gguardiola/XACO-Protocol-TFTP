from http import client
import os
from socket import *

print("##############################################")
print("#####                                    #####")
print("#####          TCP SERVER - PUT          #####")
print("#####          Alex P. y Gabriel         #####")
print("#####                v1.0                #####")
print("#####                                    #####")
print("##############################################")
print("\n")


# Default port number server will listen on
serverPort = 12004
packetSize = 1024
# Request IPv4 and TCP communication
serverSocket = socket(AF_INET,SOCK_STREAM)

#intenta bindear el puerto, EXCEPT OSERROR: si falla, cambia al puerto siguiente.
try:
	serverSocket.bind(('',serverPort))
except OSError:
	serverPort += 1
	print("[SERVIDOR]: Puerto en uso. Cambiando al {}".format(serverPort))
	serverSocket.bind(('',serverPort))


def startServer():
	# Start listening on the welcoming port
	serverSocket.listen(1)
	print ("LISTO - El servidor está escuchando por el puerto {}".format(serverPort))
	while True:
		#acepta conexión del host
		connectionSocket, addr = serverSocket.accept()
		print("CONEXIÓN ESTABLECIDA - Client IP {}".format(addr[0]))
		#recibe el mensaje con el formato: PUT [ARCHIVO] 
		clientMsg = connectionSocket.recv(packetSize).decode()
		#splitea el mensaje para comprobar si es PUT y quedarse solo con el nombre del archivo
		#de lo contrario, avisa al cliente y cierra conexión. El servidor espera conexión escuchando por el mismo puerto.
		clientMsg = clientMsg.split(" ")	

		if clientMsg[0].upper() != "PUT":
			connectionSocket.send("[SERVIDOR]: Método no compatible. Utiliza el PUT para este servidor. CERRANDO CONEXIÓN".encode())
			print("[SERVIDOR]: Método no compatible. Utiliza el PUT para este servidor. CERRANDO CONEXIÓN")
			connectionSocket.close()
			print("[SERVIDOR]: CONEXIÓN CERRADA CON {}".format(addr[0]))
			return 0
		
		connectionSocket.send("[SERVIDOR]: Preparado para recibir.".encode())
		print("[SERVIDOR]: Preparado para recibir desde {}".format(addr[0]))
		totalSize = connectionSocket.recv(packetSize).decode()
		totalSize = totalSize.split("|");totalSize = totalSize[3]

		#se queda solo con el filename
		filename = clientMsg[1]

		#recibe el primer paquete del archivo
		file = connectionSocket.recv(packetSize)
		#packetsRecv guarda la cantidad de bytes que se han descargado del archivo
		packetsRecv = len(file)
		#DEBUG - para comprobar la descarga en localhost
		#filename = "test.txt"
		#crea el fichero en local
		try:
			f = open(filename, "wb")
		except FileNotFoundError:
			print("[SERVIDOR]: No es posible crear el archivo, has puesto una ruta, crea el directorio antes.")
			return 0
		#mientras la longitud de los datos recibidos sean mayores que cero, sigue recibiendo
		while len(file) > 0:
			#escribe el paquete de datos en el archivo local
			f.write(file)
			#recibe el siguiente paquete
			file = connectionSocket.recv(packetSize)
			#informa de el proceso de descarga
			percent = round(((packetsRecv/int(totalSize))*100),2)
			print("[SERVIDOR]: Descargando [{}] {}/{} (bytes) - {}%".format(filename,packetsRecv,totalSize,percent))
			#suma el siguiente paquete en bytes al total
			packetsRecv += len(file)
			#si la longitud del ultimo recibido es cero, ya no hay más paquetes
			#informa, cierra el fd y el socket
			if len(file) == 0:
				print("{} DESCARGADO CON ÉXITO.".format(filename))
				file = bytes()

		f.close()
		connectionSocket.close()
		print("[SERVIDOR]: CONEXIÓN CERRADA CON {}".format(addr[0]))


while True:
	startServer()