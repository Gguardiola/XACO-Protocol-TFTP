from ast import Break
from ctypes import WinError
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


def setupServer(serverPort,packetSize,timeOut):
	print("\n")
	print("====================================")
	print("CONFIGURACION POR DEFECTO:")
	print("====================================",end="\n")
	print("- Puerto: {}".format(serverPort))
	print("- Tamano de paquete: {}".format(packetSize))
	print("- TimeOut (ms): {}".format(timeOut/1000))
	print("====================================",end="\n")
	opt = input("CAMBIAR CONFIGURACION?(y/n): ")
	
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
		print("[CLIENTE]: USANDO LA CONFIGURACION POR DEFECTO!!!")
		return serverPort, packetSize, timeOut

def createDir(filename):
	try:
		path = filename.split("/");path = path[:-1];path = "/".join(path)
		if not os.path.exists(path): os.makedirs(path)
	except PermissionError as e:
		generateERR(2)
		sys.exit()
	except Exception as e:
		generateERR_undefined(0,str(e))
		sys.exit()
		
	print("[SERVIDOR]: Creando directorio {}".format(path))

def generateACK(blockNumber):

	#OP CODE
	ackPacket = bytearray();ackPacket.append(0);ackPacket.append(4)
	#BLOCK NUMBER
	ackPacket += blockNumber.to_bytes(2,'big')
	print("[SERVIDOR]: Enviando ACK {}".format(blockNumber))
	serverSocket.sendto(ackPacket, clientAddress)

def generateOACK():

	## OPCODE | blksize | 0 | data1 | 0 | timeout | 0 | data2 | 0 | ...
	oackPacket = bytearray();oackPacket.append(0);oackPacket.append(6)
	oackPacket += bytearray(bytes('blksize','utf-8'));oackPacket.append(0)
	auxPacketSize = str(packetSize)
	oackPacket +=  bytearray(auxPacketSize.encode("utf-8"));oackPacket.append(0)
	oackPacket += bytearray(bytes('timeout','utf-8'));oackPacket.append(0)
	auxTimeOut = str(timeOut)
	oackPacket += bytearray(auxTimeOut.encode("utf-8"));oackPacket.append(0)
	print("[SERVIDOR]: Enviando OACK")
	serverSocket.sendto(oackPacket, clientAddress)

def generateERR(errCode):
	## OPCODE | errCode | errMsg | 0 | ...
	errCode = str(errCode)
	errPacket = bytearray();errPacket.append(0);errPacket.append(5)
	errPacket += bytearray(errCode.encode("utf-8"))
	errPacket += bytearray(bytes(serverOptions.get('ERROR_PROMPT', '{}'.format(errCode)), "utf-8"))
	errPacket.append(0)
	print("[SERVIDOR]: {}".format(serverOptions.get('ERROR_PROMPT', '{}'.format(errCode)), "utf-8"))
	print("[SERVIDOR]: Enviando ERR {}".format(errCode))
	serverSocket.sendto(errPacket, clientAddress)

#sobrecarga funcion generateERR
def generateERR_undefined(errCode, errMsg):
	## OPCODE | errCode | errMsg | 0 | ...
	errCode = str(errCode)
	errPacket = bytearray();errPacket.append(0);errPacket.append(5)
	errPacket += bytearray(errCode.encode("utf-8"))
	errPacket += bytearray(errMsg.encode("utf-8"))
	errPacket.append(0)
	print("[SERVIDOR]: {}".format(errMsg))
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
	generateOACK()
	try:
		if mode == "netascii":		f = open(filename, "r")
		else:						f = open(filename, "rb")

		blockNumber = 1
		data = f.read(packetSize)

		if len(data) == 0:
			sendDATA(blockNumber, bytes("", "utf-8"))	
			WaitACK, clientAddress = serverSocket.recvfrom(packetSize*2)

		while True:
			
			#Espera al ACK
			WaitACK, clientAddress = serverSocket.recvfrom(packetSize*2)
			print("[SERVIDOR]: Recibe ACK {}".format((WaitACK[2]<<8) + WaitACK[3]))
			opCode = int.from_bytes(WaitACK[:2], "big")

			if opCode == packetType["ACK"]:
				blockNumberACK = int.from_bytes(WaitACK[2:], "big")
				#print("[SERVIDOR]: Recibe ACK {}".format(blockNumberACK))
				if blockNumberACK == blockNumber:
					data = f.read(packetSize)
					blockNumber += 1
					blockNumber = blockNumber%65536
					#Como siempre empieza en 1
					#(Al ..35 puede llegar, el ..36 sería un 1)
					if blockNumber == 0:
						blockNumber += 1
				elif blockNumberACK != 0:
					print("[SERVIDOR]: ACK incorrecto. Se esperaba {}".format(blockNumber))
			
			if len(data) == 0:
				break
			#ENVIA DATA
			if mode == 'netascii':		sendDATA(blockNumber, bytes(data,encoding='utf-8'))
			else:						sendDATA(blockNumber, data)		
	
		print("[SERVIDOR]: {} ENVIADO CON EXITO A {}".format(filename,clientAddress))
		serverSocket.sendto(bytes(), clientAddress)
		f.close()
			
	except FileNotFoundError:
		generateERR(1)
		sys.exit()
	except Exception as e:
		generateERR_undefined(0,str(e))
		f.close()
		sys.exit()

def generatePUT(filename):

	generateOACK()
	try:
		if mode == 'netascii':		
			if "/" in filename and not os.path.exists(filename):
				createDir(filename)
			elif os.path.exists(filename): 
				generateERR(6)
				sys.exit()

			f = open(filename,'w') 
		else:
			if "/" in filename and not os.path.exists(filename):
				createDir(filename)
			elif os.path.exists(filename): 
				generateERR(6)
				sys.exit()

			f = open(filename,'wb')
	except PermissionError:
		generateERR(2)
		sys.exit()
	except Exception as e:
		generateERR_undefined(0,str(e))
		sys.exit()


	blockNumber = 0
	while True:
		serverSocket.settimeout(timeOut/1000)	# 0.00005
		
		try:
			data, serverAddress = serverSocket.recvfrom(packetSize*2)
			serverSocket.settimeout(None)
			if len(data) == 0:	break

			blockNumber = int.from_bytes(data[2:4], "big")
			print("[SERVIDOR]: Recibe DATA {}".format(blockNumber))
			newData = data[4:]
			try:
				if mode == "netascii":		f.write(newData.decode("utf-8"))
				else:						f.write(newData)
			except OSError as e:
					if e.errno == 28: generateERR(3)
					else:		      generateERR_undefined(0,str(e))
					sys.exit()

			except Exception as e:
				generateERR_undefined(0,str(e))
				sys.exit()			
						
			generateACK(blockNumber)
		except timeout:
			print("[SERVIDOR]: Error en la entrega de datos. TIME OUT.")
			generateACK(blockNumber)
			serverSocket.settimeout(None)
			data, serverAddress = serverSocket.recvfrom(packetSize*2)
		except Exception as e:
			generateERR_undefined(0,str(e))
			sys.exit()			
			
	print("[SERVIDOR]: {} DESCARGADO CON EXITO!".format(filename))
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
	
	#opCode
	opCode = int.from_bytes(requestType[:2],"big")
	
	#filename
	splittedType = requestType.split(b'\x00')	#Para coger los strings
	#print(splittedType)					#Para ver como están spliteados los strings
	filename = splittedType[1].decode()
	filename = filename[1:]
	#print(filename)						#para ver el nombre del archivo

	#mode
	mode = splittedType[2].decode()
	#print(mode)							#para ver cual es el modo

	#packetSize
	bytePacketSize = requestType.split(b'blksize')
	#Split del blksize
	#print(bytePacketSize)				#para ver como se divide con la palabra blksize
	bytesSize = bytePacketSize[1]	#Post split
	bytesSize = bytesSize[1:3]		#Los dos bytes
	packetSizeClient = int.from_bytes(bytesSize, "big")
	#print("PS: {}".format(packetSize))	#para ver cuánto da el packet size

	#timeOut
	byteTimeOut = requestType.split(b'timeout')
	#Split del timeout
	#print(byteTimeOut)					#para ver como se divide con la palabra timeout
	bytesTimeOut = byteTimeOut[1]	#Post split
	bytesTimeOut = bytesTimeOut[1:3]	#Los dos bytes
	timeOutClient = int.from_bytes(bytesTimeOut,"big")
	#print("TO: {}".format(timeOut))	#para ver cuánto da el time out

	if packetSize != packetSizeClient or timeOut != timeOutClient:
		print("[SERVIDOR]: Error en el negocio de datos")
		generateERR(4)
		break
	#else entra a get put
	if 		opCode == packetType["RRQ"]: 	generateGET(filename) 	#RRQ	
	elif 	opCode == packetType["WRQ"]:  	generatePUT(filename) 	#WRQ
	else:
		generateERR(5)
