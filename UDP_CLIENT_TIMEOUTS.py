from socket import *                                    
import os
import sys
import configparser
import time

print("##############################################")
print("#####                                    #####")
print("#####          UDP CLIENT - GET/PUT      #####")
print("#####          Alex P. y Gabriel         #####")
print("#####            v4.0  RELEASE           #####")
print("#####                                    #####")
print("##############################################")

DEBUG_MODE = False

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

serverName = serverOptions.get('SERVEROPTIONS', 'serverName')
serverPort =int(serverOptions.get('SERVEROPTIONS', 'serverPort'))
opCode = int(serverOptions.get('SERVEROPTIONS', 'opCode'))
packetSize = int(serverOptions.get('SERVEROPTIONS', 'packetSize'))
mode = serverOptions.get('SERVEROPTIONS', 'mode')

def setupClient(serverName, serverPort, packetSize, mode):
	print("##############################################")
	print("Opciones de configuracion por defecto:")
	print("Nombre del servidor: {}".format(serverName))
	print("- Puerto: {}".format(serverPort))
	print("- Tamano de paquete: {}".format(packetSize))
	print("- Modo: {}".format(mode))
	print("")
	opt = input("Cambiar opciones? (y/n): ")
	
	if opt.lower() == 'y':
		try:
			serverName = input("Nombre del servidor: ")
			serverPort = int(input("Puerto: "))
			packetSize = int(input("Tamano de paquete: "))
			mode = input("Modo (octet/netascii): ");mode = mode.lower()
			if len(str(serverName)) == 0: serverName = serverOptions.get('SERVEROPTIONS', 'serverName')
			if len(str(serverPort)) == 0: serverPort =int(serverOptions.get('SERVEROPTIONS', 'serverPort'))
			if len(str(packetSize)) == 0: packetSize =int(serverOptions.get('SERVEROPTIONS', 'packetSize'))
			if len(str(mode)) == 0: mode = serverOptions.get('SERVEROPTIONS', 'mode')
			return serverName, serverPort, packetSize, mode
		except Exception as e:
			print("ERROR - Opciones incorrectas. {}".format(e))
			serverName = 0
			return serverName, serverPort, packetSize, mode
		
	else:
		print("Usando configuración por defecto.")
		return serverName, serverPort, packetSize, mode

def generateERR(errCode):
	## OPCODE | errCode | errMsg | 0 | ...
	errCode = str(errCode)
	errPacket = bytearray();errPacket.append(0);errPacket.append(5);errPacket += errCode.to_bytes(2,'big')
	errPacket += bytearray(bytes(serverOptions.get('ERROR_PROMPT', '{}'.format(errCode))));errPacket.append(0)
	print("[CLIENTE]: {}".format(serverOptions.get('ERROR_PROMPT', '{}'.format(errCode))))
	print("[CLIENTE]: Enviando ERR {}".format(errCode))
	clientSocket.sendto(errPacket, serverAddress)

def getFile():

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
		if opCode == packetType['WRQ']:	
			#comprobar si el archivo existe
			pass

	return filename
	
def generateRRQ_WRQ(filename):

	#OP CODE
	xrqPacket = bytearray();xrqPacket.append(0);xrqPacket.append(opCode)
	#FILENAME | 0 | MODE | 0
	xrqPacket += bytearray(filename.encode('utf-8'));xrqPacket.append(0);xrqPacket += bytearray(bytes(mode, 'utf-8'));xrqPacket.append(0)
	
	clientSocket.sendto(xrqPacket, serverAddress)

def generateACK(blockNumber):

	#OP CODE
	ackPacket = bytearray();ackPacket.append(0);ackPacket.append(4)
	#BLOCK NUMBER
	ackPacket += blockNumber.to_bytes(2,'big')
	
	print("[CLIENTE]: Enviando ACK {}".format(blockNumber))
	clientSocket.sendto(ackPacket, serverAddress)

def sendDATA(blockNumber, data):

	#OP CODE
	dataPacket = bytearray();dataPacket.append(0);dataPacket.append(3)
	#BLOCK NUMBER | N DATA
	dataPacket += blockNumber.to_bytes(2,'big');dataPacket += bytes(data)

	print("[CLIENTE]: Enviando DATA {}".format(blockNumber))
	clientSocket.sendto(dataPacket, serverAddress)
	#Try except para error entrega 4

def generateGET():
	
	save_file = getFile()
	generateRRQ_WRQ(save_file)
	#DEBUG
	if DEBUG_MODE: filename = str(serverOptions.get('SERVEROPTIONS', 'test_get'))
	else:		filename = save_file
	if mode == "octet":		f = open(filename, "wb")
	else:					f = open(filename, "w")

	#Try except para error entrega 4
	#Primer paquete


	data, serverAddress = clientSocket.recvfrom(packetSize*2)
	while len(data[4:]) > 0:
		clientSocket.settimeout(0.1000)
		try:
			blockNumber = int.from_bytes(data[2:4], "big")
			print("[CLIENTE]: Recibe DATA {}".format(blockNumber))
			newData = data[4:]
			if mode == "netascii":		f.write(newData.decode("utf-8"))
			else:						f.write(newData)

			
			generateACK(blockNumber)

			data, serverAddress = clientSocket.recvfrom(packetSize*2)
			clientSocket.settimeout(None)
		except:
			print("[CLIENTE]: Error en la entrega de datos.")
			generateACK(blockNumber)
			clientSocket.settimeout(None)
			data, serverAddress = clientSocket.recvfrom(packetSize*2)

	print("{} DESCARGADO CON ÉXITO.".format(filename))
	f.close()	

def generatePUT():
	#DEBUG
	filename = getFile()
	if DEBUG_MODE: save_file = str(serverOptions.get('SERVEROPTIONS', 'test_put'))
	else:		   save_file = filename
	
	generateRRQ_WRQ(save_file)
	if mode == "octet":		f = open(filename,"rb")
	else:					f = open(filename,"r")

	#Try except para error entrega 4
	blockNumber = 1
	data = f.read(packetSize)

	if len(data) == 0:
		sendDATA(blockNumber, bytes("", "utf-8"))
		WaitACK, serverAddress = clientSocket.recvfrom(packetSize*2)


	while True:
		#Espera al ACK
		WaitACK, serverAddress = clientSocket.recvfrom(packetSize*2)
		print("[CLIENTE]: Recibe ACK {}".format( (WaitACK[2]<<8) +WaitACK[3]))
		opCode = int.from_bytes(WaitACK[:2], "big")

		if len(data) == 0:
			break

		if opCode == packetType["ACK"]:
			ACKErr = int.from_bytes(WaitACK[2:], "big")
			if ACKErr == blockNumber:
				data = f.read(packetSize)
				blockNumber += 1
				blockNumber = blockNumber%65536
				#Como siempre empieza en 1
				#(Al 35 puede llegar, el 36 sería un 1)
				if blockNumber == 0:
					blockNumber += 1
			elif ACKErr != 0:
				print("[CLIENTE]: ACK INCORRECTO. Se esperaba {}".format(blockNumber))
		#else no has recibido un ACK -> tenemos un error
		if mode == "octet":		sendDATA(blockNumber, data)
		else:					sendDATA(blockNumber, bytes(data, encoding="utf-8"))

	print("[CLIENTE]: Archivo enviado con éxito!")
	clientSocket.sendto(bytes(), serverAddress)
	f.close()

#MAIN
############################################################################################################################

clientSocket = socket(AF_INET, SOCK_DGRAM)
while True:
	serverName, serverPort, packetSize, mode = setupClient(serverName, serverPort, packetSize, mode)
	if serverName != 0:
		opt = input("Debug mode? (y/n): ")
		if opt.lower() == "y": DEBUG_MODE = True;print("MODO DEBUG ACTIVADO!")
		break

serverAddress = (serverName, serverPort)

print("Servidor {}:{}".format(serverName, serverPort))
print("##############################################")
print("MODE: {}".format(mode))
print("Tamaño de paquetes: {}".format(packetSize))
while True:		
	method = str(input("Metodo? [GET/PUT]: "))
	if method.lower() == "get" or method.lower() == "put":
		break

if method.lower() == "put":
	opCode = packetType['WRQ']	#1
	generatePUT()
elif method.lower() == "get":
	opCode = packetType['RRQ']	#2
	generateGET()

