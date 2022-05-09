from contextlib import nullcontext
from socket import *
import os
import configparser 
import sys

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

def generateACK(blockNumber):
	ackPacket = bytearray()
	ackPacket.append(0)
	ackPacket.append(4)
	ackPacket += blockNumber.to_bytes(2,'big')
	print("ACK, {}".format(blockNumber))

	serverSocket.sendto(ackPacket, clientAddress)

def sendDATA(blockNumber, data):
	dataPacket = bytearray()
	# Los 2 primeros bytes de codigo
	dataPacket.append(0)
	dataPacket.append(3)
	dataPacket += blockNumber.to_bytes(2,'big')
	dataPacket = bytes(data)

	print("INFO ---> ",len(dataPacket))
	#print("DATAencode ------------------",len(data.encode()),"/", len(data),"/",len(bytes(data)))
	serverSocket.sendto(dataPacket, clientAddress)
	print("[SERVIDOR]: Enviando DATA {}".format(blockNumber))
	
def generateGET(filename):			
	try:
		f = None
		if mode == "netascii":
			f = open(filename, "r")
		elif mode == "octet":
			f = open(filename, "rb")

		blockNumber = 1
		data = f.read(packetSize)
		
		if len(data) == 0:
			sendDATA(blockNumber, bytes())	
			waitACK, clientAddress = serverSocket.recvfrom(4)
		while( len(data) > 0):
			#ENVIA DATA
			if mode == 'netascii': # En netascii
				sendDATA(blockNumber, bytes(data,encoding='utf8'))
			else:
				sendDATA(blockNumber, data) # Octal		

			#ESPERA ACK
			waitACK, clientAddress = serverSocket.recvfrom(65535)
			opCode = int.from_bytes(waitACK[:2],"big")

			if opCode == packetType["ACK"]: #RECIBIR ACK
				blockNumberACK = int.from_bytes(waitACK[2:],"big")
				print("ACK, {}".format(blockNumberACK))
				if blockNumberACK == blockNumber:
					data = f.read(packetSize)
					blockNumber += 1
					blockNumber = blockNumber%65535
					if blockNumber == 0: blockNumber +=1
		print("[SERVIDOR]: {} ENVIADO CON EXITO A {}".format(filename,clientAddress))
		f.close()
			
	except FileNotFoundError:
		print("[SERVIDOR]: No se encuentra el fichero en el servidor!.")
		return 0 #PONER USAGE	#Arregla un bug, si no hay break, como el cliente tiene 2 inputs (name.txt y sizePacket) detecta el sizePacket como segundo nombre de archivo

def generatePUT(filename):

	generateACK(0)
	try:
		if mode == 'netascii':
			f = open(filename,'w') 
		else:
			f = open(filename,'wb')

		#AQUI SE PODRIA HACER UN TRACTA DE ERROR SI EL SEVIDOR NO ENCUENTRA EL FICHERO (data = paquet error)
		while True:
			data, serverAddress = serverSocket.recvfrom(65535)
			blockNumber = int.from_bytes(data[2:4], "big")
			f.write(data[4:])
			generateACK(blockNumber)
			if len(data[4:]) < packetSize: # La longitud de los datos va de 0 bytes al tamaño del packetsize. Si tiene packetsize bytes de longitud, el bloque no será el último bloque de datos.
				break
			# Tenemos el fichero entero en memoria (no optimo para archivos muy grandes)
		data, serverAddress = serverSocket.recvfrom(65535) #PARA EL ULTIMO QUE ES VACIO 

		print(f"Fichero guardado en: {filename}!")
		f.close() # Cerramos el archivo	
	except:
		print("ERROR!")
		
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
	opCode = int.from_bytes(requestType[:2],"big")
	print("TRAMA: ", requestType)
	requestType = requestType[2:]
	requestType = requestType.split(b'\x00') #REVISAR ESTO ES MUY TRYHARD
	filename = requestType[0]
	filename = filename.decode()
	mode = requestType[1].decode()

	if 		opCode == packetType["WRQ"]: 	generateGET(filename) 	#RRQ	
	elif 	opCode == packetType["RRQ"]:  	generatePUT(filename) 	#WRQ
