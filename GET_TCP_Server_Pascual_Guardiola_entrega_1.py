from http import client
import os
from socket import *

print("##############################################")
print("#####                                    #####")
print("#####          TCP SERVER - GET          #####")
print("#####          Alex P. y Gabriel         #####")
print("#####                v1.0                #####")
print("#####                                    #####")
print("##############################################")
print("\n")

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
		#recibe el mensaje con el formato: GET [ARCHIVO] 
		clientMsg = connectionSocket.recv(packetSize).decode()
		#splitea el mensaje para comprobar si es GET y quedarse solo con el nombre del archivo
		#de lo contrario, avisa al cliente y cierra conexión. El servidor espera conexión escuchando por el mismo puerto.
		clientMsg = clientMsg.split(" ")	

		if clientMsg[0].upper() != "GET":
			connectionSocket.send("[SERVIDOR]: Método no compatible. Utiliza el GET para este servidor. CERRANDO CONEXIÓN".encode())
			print("[SERVIDOR]: Método no compatible. Utiliza el GET para este servidor. CERRANDO CONEXIÓN")
			connectionSocket.close()
			print("[SERVIDOR]: CONEXIÓN CERRADA CON {}".format(addr[0]))
			return 0
		
		#se queda solo con el filename
		clientMsg = clientMsg[1]

		#busca si existe el archivo. EXCEPT FILENOTFOUNDERROR: cierra conexión e informa al cliente.
		try:
			f = open(clientMsg,"rb")
			#lee los n primeros bytes -> Va leyendo el archivo segmentado para enviarlo en paquetes al cliente
			file = f.read(packetSize)
			#recoge la mida total para informar cuanto queda por enviar
			totalSize = os.path.getsize(clientMsg)
			#informa al cliente de que el se ha encontrado.
			#de paso le envia la mida total del archivo
			connectionSocket.send("[SERVIDOR]: Fichero: |{}| Peso: |{}| encontrado, enviando...".format(clientMsg,totalSize).encode())
		except FileNotFoundError:
			connectionSocket.send("[SERVIDOR]: No se encuentra el fichero en el servidor!. CERRANDO CONEXIÓN".encode())
			print("[SERVIDOR]: No se encuentra el fichero en el servidor!. CERRANDO CONEXIÓN con {}".format(addr[0]))
			connectionSocket.close()
			print("[SERVIDOR]: CONEXIÓN CERRADA CON {}".format(addr[0]))
			return 0
		#packetsSended guarda el avance del envio del archivo
		packetsSended = len(file)
		#mientras no se haya leido todo el archivo, sigue enviando

		try:
			while len(file) > 0:
				percent = round(((packetsSended/int(totalSize))*100),2)
				print("[SERVIDOR]: Enviando [{}] {}/{} (bytes) - {}%".format(clientMsg,packetsSended,totalSize,percent))
				#envia el paquete
				connectionSocket.send(file)
				#lee los siguientes n bytes del paquete
				file = f.read(packetSize)
				#aumenta la cantidad de bytes enviados
				packetsSended += len(file)
				#si el la longitud del fichero es cero, signfiica que ya ha enviado todo. Envia byte de finalización
				if len(file) == 0:
					print("[SERVIDOR]: {} ENVIADO CON EXITO A {}".format(clientMsg,addr[0]))
					connectionSocket.send(bytes())	
		except ConnectionResetError as e:
			print(e)
			f.close()
			return 0
		except ConnectionAbortedError as e:
			print(e)
			f.close()
			return 0

		f.close()
		connectionSocket.close()
		print("[SERVIDOR]: CONEXIÓN CERRADA CON {}".format(addr[0]))

while True:
	startServer()