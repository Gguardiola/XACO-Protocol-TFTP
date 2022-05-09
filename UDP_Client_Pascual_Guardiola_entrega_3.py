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
	
def generateRRQ_WRQ():
	xrqPacket = bytearray()
	xrqPacket.append(0)
	xrqPacket.append(opCode)
	xrqPacket += bytearray(filename.encode('utf-8'))
	xrqPacket.append(0)
	xrqPacket +=  bytearray(bytes(mode, 'utf-8'))
	xrqPacket.append(0)
	clientSocket.sendto(xrqPacket, serverAddress)

def generateACK(blockNumber):

	ackPacket = bytearray()
	ackPacket.append(0)
	ackPacket.append(4)
	ackPacket += blockNumber.to_bytes(2,'big')
	print("ACK, {}".format(blockNumber))
	clientSocket.sendto(ackPacket, serverAddress)
	#Try except para error entrega 4

def generateDATA(blockNumber, data):
	dataPacket = bytearray()
	dataPacket.append(0)
	dataPacket.append(3)
	dataPacket += blockNumber.to_bytes(2,'big')
	dataPacket = bytes(data)
	clientSocket.sendto(dataPacket, serverAddress)
	print("Enviando DATA {}".format(blockNumber))
	#Try except para error entrega 4

def generateGET():

		#DEBUG
		filename = "test.txt"
		if mode == "octet":
			f = open(filename, "wb")
		else:
			f = open(filename, "w")
		data, serverAddress = clientSocket.recvfrom(65535)

		while len(data[4:]) > 0:
			#RECIBE DATA este
			blockNumber = int.from_bytes(data[2:4], "big")
			print("DATA, {}".format(blockNumber))
			#GENERATE ACK
			generateACK(blockNumber)
			f.write(data[4:].decode())
			data, serverAddress = clientSocket.recvfrom(65535)
						
		print("{} DESCARGADO CON ÉXITO.".format(filename))	
		f.close()	



clientSocket = socket(AF_INET, SOCK_DGRAM)
serverAddress = (serverName, serverPort)

print("Servidor {}:{}".format(serverName, serverPort))
print("##############################################")
		
method = str(input("Metodo? [GET/PUT]: "))

##ELEGIR NETASCII O OCTET

if method == "GET":
	opCode = packetType['WRQ']
	filename = getFile()
	generateRRQ_WRQ()
	generateGET()
	
elif method == "PUT":
	opCode = packetType['RRQ']
	filename = getFile()
	generateRRQ_WRQ()
	##generatePUT()
	pass
	


