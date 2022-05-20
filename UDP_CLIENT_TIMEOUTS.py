import opcode
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
timeOut = int(serverOptions.get('SERVEROPTIONS', 'timeOut'))

def setupClient(serverName, serverPort, packetSize, mode,timeOut):
	print("##############################################")
	print("Opciones de configuracion por defecto:")
	print("Nombre del servidor: {}".format(serverName))
	print("- Puerto: {}".format(serverPort))
	print("- Tamano de paquete: {}".format(packetSize))
	print("- Modo: {}".format(mode))
	print("- TimeOut (ms): {}".format(timeOut/1000))
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
			if len(str(timeOut)) == 0: timeOut =int(serverOptions.get('SERVEROPTIONS', 'timeOut'))
			return serverName, serverPort, packetSize, mode, timeOut
		except Exception as e:
			print("ERROR - Opciones incorrectas. {}".format(e))
			serverName = 0
			return serverName, serverPort, packetSize, mode, timeOut
		
	else:
		print("Usando configuración por defecto.")
		return serverName, serverPort, packetSize, mode, timeOut

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

		if opCode == packetType['WRQ']:	

			if not os.path.exists(filename):
				print("[CLIENTE]: ERROR - EL ARCHIVO NO EXISTE.")
				return -1
		
		return filename
def createDir(save_file):
	path = save_file.split("/");path = path[:-1];path = path[0]
	os.makedirs(path)
	print("[CLIENTE]: Creando directorio {}".format(path))

def raiseERR(data):
	splitErr = data[2:]
	#Aqui tenemos el mensaje sin el opcode
	codeErr = splitErr[0:1]
	codeErr = int(codeErr)
	#En el codeErr tenemos el 4
	strErr = splitErr.split(b"\x00")
	strErr = strErr[0]
	strErr = strErr[1:].decode("utf-8")
	#En el strErr tenemos el string del Error
	print("[CLIENTE]: {}".format(strErr))

def generateRRQ_WRQ(filename):
	print("[CLIENTE]: Enviando RRQ")
	#OP CODE
	xrqPacket = bytearray();xrqPacket.append(0);xrqPacket.append(opCode)
	#FILENAME | 0 | MODE | 0
	xrqPacket += bytearray(filename.encode('utf-8'));xrqPacket.append(0)
	xrqPacket += bytearray(bytes(mode, 'utf-8'));xrqPacket.append(0)
	xrqPacket += bytearray(bytes('blocksize', 'utf-8'))
	xrqPacket.append(0);xrqPacket += packetSize.to_bytes(2,'big')
	xrqPacket.append(0)
	xrqPacket += bytearray(bytes('timeout', 'utf-8'));xrqPacket.append(0)
	xrqPacket += timeOut.to_bytes(2,'big');xrqPacket.append(0)
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
	
	filename = getFile()
	

	#DEBUG
	if DEBUG_MODE: save_file = str(serverOptions.get('SERVEROPTIONS', 'test_get'))
	else:		save_file = filename
	if os.path.exists(save_file):
		print("[CLIENTE]: Error: ARCHIVO YA EXISTE")
		sys.exit()

	if mode == "octet":
		#si save_file tiene "/", es directorio, entonces lo crea		
		if "/" in save_file and not os.path.exists(save_file):
			createDir(save_file)

		f = open(save_file, "wb")

	else:
		#si save_file tiene "/", es directorio, entonces lo crea		
		if "/" in save_file and not os.path.exists(save_file):
			createDir(save_file)
		
		f = open(save_file, "w")

	generateRRQ_WRQ(filename)
	#Recibe OACK
	data, serverAddress = clientSocket.recvfrom(512)
	#OPCODE
	opCode = int.from_bytes(data[:2], 'big')

	while len(data[4:]) > 0:
		clientSocket.settimeout(timeOut/10)	#0.1000
		try:
			if opCode == packetType['DATA']:
				blockNumber = int.from_bytes(data[2:4], "big")
				print("[CLIENTE]: Recibe DATA {}".format(blockNumber))
				newData = data[4:]
				try:
					if mode == "netascii":		f.write(newData.decode("utf-8"))
					else:						f.write(newData)
				except OSError as e:
					if e.errno == 28:
						print("[CLIENTE]: Error: DISCO LLENO O EXCESO DE CAPACIDAD")
						return -1
				
				generateACK(blockNumber)

				data, serverAddress = clientSocket.recvfrom(packetSize*2)
				#print(len(data[4:]))
				opCode = int.from_bytes(data[:2], 'big')
				clientSocket.settimeout(None)

			elif opCode == packetType['OACK']:
				print("[CLIENTE]: Recibe OACK")
				#packetSize
				bytePacketSize = data.split(b'blocksize')
				#Split del blocksize
				strSize = bytePacketSize[1]	#Post split
				strSize = strSize[1:len(str(packetSize))+1]		#Los dos bytes
				#print(strSize)
				try:
					packetSizeServer = int(strSize)
				except:
					print("[CLIENTE]: No tenemos el mismo blocksize")
					f.close()
					sys.exit()

				#print("PS: {}".format(packetSizeServer))
				
				#timeOut
				byteTimeOut = data.split(b'timeout')
				strTimeOut = byteTimeOut[1]	#Post split
				strTimeOut = strTimeOut[1:2]	#El string con el timeout
				timeOutServer = int(strTimeOut)
				#print("TO: {}".format(timeOutServer))
				
				if packetSize != packetSizeServer or timeOut != timeOutServer:
					print("[CLIENTE]: ERROR OACK")
					f.close()
					sys.exit()
				else:
					generateACK(0)
					data, serverAddress = clientSocket.recvfrom(packetSize*2)
					#print(len(data[4:]))
					opCode = int.from_bytes(data[:2], 'big')
					clientSocket.settimeout(None)

			elif opCode == packetType['ERR']:
				raiseERR(data)	
				clientSocket.settimeout(None)
				f.close()
				sys.exit()
					
		except TimeoutError:
			print("[CLIENTE]: Error en la entrega de datos.")
			generateACK(blockNumber)
			clientSocket.settimeout(None)
			data, serverAddress = clientSocket.recvfrom(packetSize*2)
			opCode = int.from_bytes(data[:2], 'big')

	print("[CLIENTE]: {} DESCARGADO CON ÉXITO.".format(save_file))
	f.close()	

def generatePUT():
	#DEBUG
	filename = getFile()
	while filename == -1:
		filename = getFile()
		
	if DEBUG_MODE: save_file = str(serverOptions.get('SERVEROPTIONS', 'test_put'))
	else:		   save_file = filename
	
	generateRRQ_WRQ(save_file)
	#Recibe OACK
	WaitACK, serverAddress = clientSocket.recvfrom(512)
	opCode = int.from_bytes(WaitACK[:2], 'big')

	if mode == "octet":		f = open(filename,"rb")
	else:					f = open(filename,"r")
	#Try except para error entrega 4
	blockNumber = 1
	
	#if len(WaitACK) == 0:
	#	sendDATA(blockNumber, bytes("", "utf-8"))
	#	WaitACK, serverAddress = clientSocket.recvfrom(packetSize*2)


	while True:
		#HAY QUE CAMBIARLO
		if opCode == packetType["ACK"]:
			ACKErr = int.from_bytes(WaitACK[2:], "big")
			if ACKErr == blockNumber:
				if len(data) == 0:
					break
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
			#Espera al ACK
			WaitACK, serverAddress = clientSocket.recvfrom(packetSize*2)
			print("[CLIENTE]: Recibe ACK {}".format( (WaitACK[2]<<8) +WaitACK[3]))
			opCode = int.from_bytes(WaitACK[:2], "big")
		elif opCode == packetType["OACK"]:
				print("[CLIENTE]: Recibe OACK")

				#packetSize
				bytePacketSize = WaitACK.split(b'blocksize')
				#print(bytePacketSize)
				#Split del blocksize
				strSize = bytePacketSize[1]	#Post split
				strSize = strSize[1:len(str(packetSize))+1]		#Los dos bytes
				#print(strSize)
				try:
					packetSizeServer = int(strSize)
				except:
					print("[CLIENTE]: No tenemos el mismo blocksize")
					f.close()
					sys.exit()

				#print("PS: {}".format(packetSizeServer))
				
				#timeOut
				byteTimeOut = WaitACK.split(b'timeout')
				strTimeOut = byteTimeOut[1]	#Post split
				strTimeOut = strTimeOut[1:2]	#El string con el timeout
				timeOutServer = int(strTimeOut)
				#print("TO: {}".format(timeOutServer))
				
				if packetSize != packetSizeServer or timeOut != timeOutServer:
					print("[CLIENTE]: ERROR OACK")
					f.close()
					sys.exit()
				else:
					blockNumber = 1
					data = f.read(packetSize)
					if mode == "octet":		sendDATA(blockNumber, data)
					else:					sendDATA(blockNumber, bytes(data, encoding="utf-8"))
					#Espera al ACK
					WaitACK, serverAddress = clientSocket.recvfrom(packetSize*2)
					opCode = int.from_bytes(WaitACK[:2], "big")
					if opCode == packetType['ACK']:
						print("[CLIENTE]: Recibe ACK {}".format( (WaitACK[2]<<8) +WaitACK[3]))
					#else ha entrado un ERROR en vez de ACK
					clientSocket.settimeout(None)			
		elif opCode == packetType['ERR']:
				raiseERR(WaitACK)	
				clientSocket.settimeout(None)
				f.close()
				sys.exit()
	print("[CLIENTE]: {} ENVIADO CON EXITO A {}".format(filename,serverAddress))
	clientSocket.sendto(bytes(), serverAddress)
	f.close()

#MAIN
############################################################################################################################

clientSocket = socket(AF_INET, SOCK_DGRAM)
while True:
	serverName, serverPort, packetSize, mode, timeOut = setupClient(serverName, serverPort, packetSize, mode, timeOut)
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

