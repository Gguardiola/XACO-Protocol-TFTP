from logging.handlers import WatchedFileHandler
from socket import *
from struct import *                                         
import os, sys, random, configparser


print("##############################################")
print("#####                                    #####")
print("#####          UDP CLIENT - GET/PUT      #####")
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
serverName = serverOptions.get('SERVEROPTIONS', 'serverName')
serverPort =int(serverOptions.get('SERVEROPTIONS', 'serverPort'))
opCode = int(serverOptions.get('SERVEROPTIONS', 'opCode'))
packetSize = int(serverOptions.get('SERVEROPTIONS', 'packetSize'))
mode = serverOptions.get('SERVEROPTIONS', 'mode')


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
	xrqPacket = bytearray()
	xrqPacket.append(0)
	xrqPacket.append(opCode)
	xrqPacket += bytearray(filename.encode('utf-8'))
	xrqPacket.append(0)
	xrqPacket += bytearray(bytes(mode, 'utf-8'))
	xrqPacket.append(0)
	clientSocket.sendto(xrqPacket, serverAddress)

def generateACK(blockNumber):

	ackPacket = bytearray()
	ackPacket.append(0)
	ackPacket.append(4)
	ackPacket += blockNumber.to_bytes(2,'big')
	print("Enviando ACK {}".format(blockNumber))
	clientSocket.sendto(ackPacket, serverAddress)
	#Try except para error entrega 4

def sendDATA(blockNumber, data):
	dataPacket = bytearray()
	dataPacket.append(0)
	dataPacket.append(3)
	dataPacket += blockNumber.to_bytes(2,'big')
	dataPacket += bytes(data)
	clientSocket.sendto(dataPacket, serverAddress)
	print("Enviando DATA {}".format(blockNumber))
	#Try except para error entrega 4

def generateGET():
	#DEBUG
	save_file = getFile()
	generateRRQ_WRQ(save_file)
	filename = "test.txt"
	if mode == "octet":
		f = open(filename, "wb")
	else:
		f = open(filename, "w")
	#Try except para error entrega 4
	#Primer paquete
	data, serverAddress = clientSocket.recvfrom(packetSize*2)
	while len(data[4:]) > 0:
		#Numero de secuencia del paquete
		blockNumber = int.from_bytes(data[2:4], "big")
		print("DATA recibido: {}".format(blockNumber))
		#Escribo el data en el .txt
		ESCRIBE = data[4:]
		if mode == "netascii":
			f.write(ESCRIBE.decode("utf-8"))
		else:
			f.write(ESCRIBE)
		#Envío el ACK del DATA correspondiente
		generateACK(blockNumber)
		#Cojo un nuevo data
		data, serverAddress = clientSocket.recvfrom(packetSize*2)
	#Ya se ha descargado todo el archivo			
	print("{} DESCARGADO CON ÉXITO.".format(filename))
	#Cerramos archivo
	f.close()	

def generatePUT():
	save_file = "test2.txt"
	filename = getFile()
	generateRRQ_WRQ(save_file)
	if mode == "octet":
		f = open(filename,"rb")
	else:
		f = open(filename,"r")
	#Try except para error entrega 4
	blockNumber = 1	#El ACK siempre empezará con un 1
	data = f.read(packetSize-4)
	#Si el fichero no tiene nada
	if len(data) == 0:
		sendDATA(blockNumber, bytes("", "utf-8"))
		WaitACK, serverAddress = clientSocket.recvfrom(packetSize*2)
	#Si el fichero no está vacío
	while True:
		#Espera al ACK
		WaitACK, serverAddress = clientSocket.recvfrom(packetSize*2)
		print("ACK recibido {}".format( (WaitACK[2]<<8) +WaitACK[3]))
		opCode = int.from_bytes(WaitACK[:2], "big")

		if len(data) == 0:
			break
		#Podemos recibir un ACK o un error
		if opCode == packetType["ACK"]:
			ACKErr = int.from_bytes(WaitACK[2:], "big")
			#Si es un ACK, todo bien
			if ACKErr == blockNumber:
				data = f.read(packetSize-4)
				blockNumber += 1
				blockNumber = blockNumber%65536
				#Como siempre empieza en 1
				#(Al 35 puede llegar, el 36 sería un 1)
				if blockNumber == 0:
					blockNumber += 1
		#else no has recibido un ACK -> tenemos un error
		if mode == "octet":
			sendDATA(blockNumber, data)
		else:
			sendDATA(blockNumber, bytes(data, encoding="utf-8"))
	#print("ACK recibido {}".format( (WaitACK[2]<<8) +WaitACK[3]))
	print("Fichero enviado con éxito.")
	clientSocket.sendto(bytes(), serverAddress)
	f.close()


clientSocket = socket(AF_INET, SOCK_DGRAM)
serverAddress = (serverName, serverPort)

print("Servidor {}:{}".format(serverName, serverPort))
print("##############################################")
		
method = str(input("Metodo? [GET/PUT]: "))
##ELEGIR NETASCII O OCTET
#print("generaDATA", sendDATA(10, "ABCDE"))
if method == "PUT":
	opCode = packetType['WRQ']	#1
	generatePUT()
elif method == "GET":
	opCode = packetType['RRQ']	#2
	generateGET()
print("Conexión finalizada")
clientSocket.close()
	

#WRQ -> PUT y el RRQ -> GET
