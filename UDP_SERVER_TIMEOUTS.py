import time
from socket import *
import os
import configparser 
import sys

print("##############################################")
print("#####                                    #####")
print("#####          UDP SERVER - GET/PUT      #####")
print("#####          Alex P. y Gabriel         #####")
print("#####            v4.0  RELEASE           #####")
print("#####                                    #####")
print("##############################################")

packetType = {
    'RRQ': 1,
    'WRQ': 2,
    'DATA': 3,
    'ACK': 4,
	'ERR': 5,
	'OACK': 6
}   

#Server Options
serverOptions = configparser.ConfigParser()
try:
	serverOptions.read('settings.ini')
except FileNotFoundError:
	print("ERROR - No se encuentra el archivo de configuracion.")
	sys.exit()

serverPort =int(serverOptions.get('SERVEROPTIONS', 'serverPort'))
opCode = int(serverOptions.get('SERVEROPTIONS', 'opCode'))
packetSize = int(serverOptions.get('SERVEROPTIONS', 'packetSize'))
timeOut = int(serverOptions.get('SERVEROPTIONS', 'timeOut'))
mode = serverOptions.get('SERVEROPTIONS', 'mode')


def setupServer(serverPort,packetSize):
	print("##############################################")	
	print("Opciones de configuracion por defecto:")
	print("- Puerto: {}".format(serverPort))
	print("- Tamano de paquete: {}".format(packetSize))
	print("- TimeOut (ms): {}".format(timeOut))
	print("")
	opt = input("Cambiar opciones? (y/n): ")
	
	if opt.lower() == 'y':
		try:
			serverPort = int(input("Puerto: "))
			packetSize = int(input("Tamano de paquete: "))
			timeOut = int(input("TimeOut (ms): "))
			if len(str(serverPort)) == 0: serverPort =int(serverOptions.get('SERVEROPTIONS', 'serverPort'))
			if len(str(packetSize)) == 0: packetSize =int(serverOptions.get('SERVEROPTIONS', 'packetSize'))
			if len(str(timeOut)) == 0: packetSize =int(serverOptions.get('SERVEROPTIONS', 'timeOut'))
			return serverPort, packetSize, timeOut
		except Exception as e:
			print("ERROR - Opciones incorrectas. {}".format(e))
			serverPort = packetSize = timeOut = 0
			return serverPort, packetSize, timeOut
		
	else:
		print("Usando configuración por defecto.")
		return serverPort, packetSize


def generateACK(blockNumber):

	#OP CODE
	ackPacket = bytearray();ackPacket.append(0);ackPacket.append(4)
	#BLOCK NUMBER
	ackPacket += blockNumber.to_bytes(2,'big')
	print("[SERVIDOR]: Enviando ACK {}".format(blockNumber))
	serverSocket.sendto(ackPacket, clientAddress)

def generateOACK():

	## OPCODE | blocksize | 0 | data1 | 0 | timeout | 0 | data2 | 0 | ...
	oackPacket = bytearray();oackPacket.append(0);oackPacket.append(6)
	oackPacket += bytearray(bytes('blocksize'));oackPacket.append(0)
	oackPacket += packetSize.to_bytes(2,'big');oackPacket.append(0)
	oackPacket += bytearray(bytes('timeout'));oackPacket.append(0)
	oackPacket += timeOut.to_bytes(2,'big');oackPacket.append(0)
	print("[SERVIDOR]: Enviando OACK")
	serverSocket.sendto(oackPacket, clientAddress)

def generateERR(errCode):
	## OPCODE | errCode | errMsg | 0 | ...
	errCode = str(errCode)
	errPacket = bytearray();errPacket.append(0);errPacket.append(5);errPacket += errCode.to_bytes(2,'big')
	errPacket += bytearray(bytes(serverOptions.get('ERROR_PROMPT', '{}'.format(errCode))));errPacket.append(0)
	print("[SERVIDOR]: {}".format(serverOptions.get('ERROR_PROMPT', '{}'.format(errCode))))
	print("[SERVIDOR]: Enviando ERR {}".format(errCode))
	serverSocket.sendto(errPacket, clientAddress)

def sendDATA(blockNumber, data):

	#OP CODE
	dataPacket = bytearray();dataPacket.append(0);dataPacket.append(3)
	#BLOCK NUMBER | N DATA
	dataPacket += blockNumber.to_bytes(2,'big'); dataPacket += data

	print("[SERVIDOR]: Enviando DATA {}".format(blockNumber))
	serverSocket.sendto(dataPacket, clientAddress)
	
def generateGET(filename):	

	try:
		if mode == "netascii":		f = open(filename, "r")
		else:						f = open(filename, "rb")

		blockNumber = 1
		data = f.read(packetSize)

		if len(data) == 0:
			sendDATA(blockNumber, bytes("", "utf-8"))	
			waitACK, clientAddress = serverSocket.recvfrom(packetSize*2)

		while len(data) > 0:
			#ENVIA DATA
			if mode == 'netascii':		sendDATA(blockNumber, bytes(data,encoding='utf-8'))
			else:						sendDATA(blockNumber, data)		

			#ESPERA ACK
			waitACK, clientAddress = serverSocket.recvfrom(packetSize*2)
			opCode = int.from_bytes(waitACK[:2],"big")

			if opCode == packetType["ACK"]:
				blockNumberACK = int.from_bytes(waitACK[2:],"big")
				print("[SERVIDOR]: Recibe ACK {}".format(blockNumberACK))

				if blockNumberACK == blockNumber:

					data = f.read(packetSize)
					blockNumber += 1
					blockNumber = blockNumber%65536

					if blockNumber == 0: blockNumber +=1
				else:
					print("[SERVIDOR]: ACK incorrecto. Se esperaba {}".format(blockNumber))
					
		print("[SERVIDOR]: {} ENVIADO CON EXITO A {}".format(filename,clientAddress))
		serverSocket.sendto(bytes(), clientAddress)
		f.close()
			
	except FileNotFoundError:
		print("[SERVIDOR]: No se encuentra el fichero en el servidor!.")
		return 0 #PONER USAGE

def generatePUT(filename):

	generateACK(0)

	if mode == 'netascii':		f = open(filename,'w') 
	else:						f = open(filename,'wb')

	blockNumber = 0
	while True:
		serverSocket.settimeout(0.00005)
		
		try:
			data, serverAddress = serverSocket.recvfrom(packetSize*2)
			serverSocket.settimeout(None)
			if len(data) == 0:	break

			blockNumber = int.from_bytes(data[2:4], "big")
			print("[SERVIDOR]: Recibe DATA {}".format(blockNumber))
			newData = data[4:]

			if mode == "netascii":		f.write(newData.decode("utf-8"))
			else:						f.write(newData)

			generateACK(blockNumber)
		except:
			print("[SERVIDOR]: Error en la entrega de datos.")
			generateACK(blockNumber)
			serverSocket.settimeout(None)
			data, serverAddress = serverSocket.recvfrom(packetSize*2)
			
	print("[SERVIDOR]: ARCHIVO DESCARGADOR CON EXITO!")
	f.close() 


#MAIN
############################################################################################################################
# Setup IPv4 UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
while True:
	serverPort, packetSize, timeOut = setupServer(serverPort,packetSize,timeOut)
	if serverPort != 0:
		break

# Specify the welcoming port of the server
try:
	serverSocket.bind(('', serverPort))
except OSError:
	serverPort += 1
	serverSocket.bind(('', serverPort))
	print("[SERVIDOR]: Puerto en uso. Cambiando al {}".format(serverPort))


while True:
	print ("[SERVIDOR]: LISTO - El servidor listo para recibir por el puerto {}".format(serverPort))

	#RRQ - WRQ
	requestType, clientAddress = serverSocket.recvfrom(packetSize*2)
	print("[SERVIDOR]: CONEXIÓN ESTABLECIDA - Client IP {}".format(clientAddress))
	opCode = int.from_bytes(requestType[:2],"big")
	requestType = requestType[2:]
	requestType = requestType.split(b'\x00') #REVISAR ESTO ES MUY TRYHARD
	filename = requestType[0]
	filename = filename.decode()
	mode = requestType[1].decode()

	if 		opCode == packetType["RRQ"]: 	generateGET(filename) 	#RRQ	
	elif 	opCode == packetType["WRQ"]:  	generatePUT(filename) 	#WRQ