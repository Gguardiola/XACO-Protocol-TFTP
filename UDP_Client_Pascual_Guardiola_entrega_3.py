from socket import *
import configparser
import sys


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
	ackPacket = [0,4,blockNumber.to_bytes(2,"big")]
	ackPacket = bytearray(ackPacket)
	print("ACK, {}".format(blockNumber))
	clientSocket.sendto(ackPacket, serverAddress)

def generateGET():

		#DEBUG
		filename = "test.txt"
		if mode == "octet":
			f = open(filename, "wb")
		elif mode == "netascii":
			f = open(filename, "w")
		data, serverAddress = clientSocket.recvfrom(packetSize)
		#packetsRecv = len(data)
		while len(data[4:]) > 0:
			#RECIBE DATA este
	
			blockNumber = int.from_bytes(data[2:4], "big")
			print("DATA, {}".format(blockNumber))
			#GENERATE ACK
			generateACK(blockNumber)
			f.write(data[4:])
			data, serverAddress = clientSocket.recvfrom(packetSize)
			#print("Descargando [{}] {}/{} (bytes)".format(filename,packetsRecv,totalSize))
			#packetsRecv += len(data[4:])							
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
	


