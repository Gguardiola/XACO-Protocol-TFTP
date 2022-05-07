from contextlib import nullcontext
from socket import *
import os
import configparser
import sys

from charset_normalizer import from_bytes

print("##############################################")
print("#####                                    #####")
print("#####          UDP SERVER - GET/PUT      #####")
print("#####          Alex P. y Gabriel         #####")
print("#####                v3.0                #####")
print("#####                                    #####")
print("##############################################")



packetType = {
    'RRQ': 1,
    'WRQ': 2,
    'DATA': 3,
    'ACK': 4,
}   

serverOptions = configparser.ConfigParser()
try:
	serverOptions.read('settings.ini')
except FileNotFoundError:
	print("ERROR - No se encuentra el archivo de configuracion.")
	sys.exit()

#Server Options
serverPort =int(serverOptions.get('SERVEROPTIONS', 'serverPort'))
opCode = int(serverOptions.get('SERVEROPTIONS', 'opCode'))
packetSize = int(serverOptions.get('SERVEROPTIONS', 'packetSize'))
mode = serverOptions.get('SERVEROPTIONS', 'mode')

def generateACK():
	print("IBAI LLANOS GARATEA")

def sendDATA(blockNumber, data):

	dataPacket = [0,3,blockNumber.to_bytes(2,"big"),bytes(data)]
	dataPacket = bytearray(dataPacket)

	serverSocket.sendto(dataPacket, clientAddress)
	print("[SERVIDOR]: Enviando DATA {}".format(blockNumber))



def generateGET(filename):			
			try:
				if mode == "octet":
					f = open(filename, "rb")
				elif mode == "netascii":
					f = open(filename, "r")

				blockNumber = 1
				data = f.read(packetSize)
				packetsSended = len(data)
				totalSize = os.path.getsize(filename)
				#serverSocket.sendto("encontrado |{}".format(totalSize).encode(),(clientAddress))

				while( len(data) > 0):
					percent = round(((packetsSended/int(totalSize))*100),2)
					sendDATA(blockNumber, data)
					print("[SERVIDOR]: Enviando [{}] {}/{} (bytes) - {}%".format(filename,packetsSended,totalSize,percent))	
					data = f.read(packetSize)
					packetsSended += len(data)
					waitACK, clientAddress = serverSocket.recvfrom(packetSize)
					opCode = int(from_bytes(waitACK[:2],"big"))
					if opCode == packetType["ACK"]: #RECIBIR ACK
						blockNumberACK = int(from_bytes(waitACK[2:],"big"))
						print("ACK, {}".format(blockNumberACK))
						if blockNumberACK == blockNumber:
							blockNumber += 1
							blockNumber = blockNumber%65535
							if blockNumber == 0: blockNumber +=1
								

				print("[SERVIDOR]: {} ENVIADO CON EXITO A {}".format(filename,clientAddress))
				serverSocket.sendto(bytes(), clientAddress)	#Debería de ser bytes()? (Antes estaba data)
				f.close()
					
			except FileNotFoundError:
				print("[SERVIDOR]: No se encuentra el fichero en el servidor!.")
				serverSocket.sendto(bytes(), clientAddress)
				return 0 #PONER USAGE	#Arregla un bug, si no hay break, como el cliente tiene 2 inputs (name.txt y sizePacket) detecta el sizePacket como segundo nombre de archivo

def generatePUT(filename):

			fileExistsChecker = True
			totalSize, clientAddress = serverSocket.recvfrom(packetSize)
			totalSize = totalSize.decode()
			#si lo ha encontrado, recoge el tamaño del archivo para informar del estado de la descarga
			if "encontrado" in totalSize:
				totalSize = totalSize.split("|");totalSize = totalSize[1]

			else:
				fileExistsChecker = False

			if fileExistsChecker:
				#recibimos el primer paquete
				data, clientAddress = serverSocket.recvfrom(packetSize)
				#DEBUG
				filename = "test2.txt"
				#filename = command[1]
				f = open(filename, "wb")
				packetsRecv = len(data)
				while( len(data) > 0):
					f.write(data)
					print("[SERVIDOR]:  Descargando [{}] {}/{} (bytes)".format(filename,packetsRecv,totalSize))
					data, clientAddress = serverSocket.recvfrom(packetSize)
					packetsRecv += len(data)
				#Pasa lo mismo que en el Client, recvfrom nos devuelve un 0 en data, sale del bucle y llega hasta estas líneas
				print("[SERVIDOR]: {} DESCARGADO CON ÉXITO.".format(filename))
				f.close()	
			else:
				print("[SERVIDOR]: {} NO ENCONTRADO.".format(filename))


# Setup IPv4 UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Specify the welcoming port of the server
try:
	serverSocket.bind(('', serverPort))
except OSError:
	serverPort += 1
	serverSocket.bind(('', serverPort))
	print("[SERVIDOR]: Puerto en uso. Cambiando al {}".format(serverPort))


while True:
	print ("LISTO - El servidor listo para recibir por el puerto {}".format(serverPort))

	#RRQ - WRQ
	requestType, clientAddress = serverSocket.recvfrom(65535)
	print("CONEXIÓN ESTABLECIDA - Client IP {}".format(clientAddress))
	opCode = int(from_bytes(requestType[:2],"big"))
	print("TRAMA: ", requestType)
	requestType = requestType[2:]
	requestType = requestType.split(b'\x00') #REVISAR ESTO ES MUY TRYHARD
	filename = requestType[0]
	filename = filename.decode()
	mode = requestType[1].decode()

	if 		opCode == packetType["RRQ"]: 	generatePUT(filename, serverSocket, clientAddress) 	#RRQ	
	elif 	opCode == packetType["WRQ"]:  	generateGET(filename, serverSocket, clientAddress) 	#WRQ
