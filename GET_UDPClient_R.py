# Example UDP socket client that fires some text at a server
import sys
import argparse

from socket import *


print("##############################################")
print("#####                                    #####")
print("#####          UDP CLIENT - GET          #####")
print("#####          Alex P. y Gabriel         #####")
print("#####                v1.0                #####")
print("#####                                    #####")
print("##############################################")


# Default to running on localhost, port 12000
serverName = 'localhost'
serverPort = 12000
packetSize = 1024
# Request IPv4 and UDP communication
clientSocket = socket(AF_INET, SOCK_DGRAM)
#error = False
# Open the TCP connection to the server at the specified port 
#Duda gabriel: Hace falta? copiar y pegar el try except del tcp get

# Read in some text from the user
client_msg = input('Escriu command:')
command = client_msg.split()
if len(command) > 0:
	print("jolines")
	if command[0] == 'get':
		print("twuitter")
		print("%i" %len(command))
		#if len(command) != 3:
		#	error = true
		#if not error:
		if len(command) == 3:
			#enviamos el comando con el fichero que vamos a subir
			print("Freeman")
			clientSocket.sendto(client_msg.encode(),(serverName,serverPort))
			print("porfavor")
			# TODO: receive ok msg
			# receive file
			data, serverAddress = clientSocket.recvfrom(packetSize)
			print("biblioteca")
			try:
				
				# TODO: if file not exists, what happends with the client
				f = open(command[1], "wb")
				
				while data:
					f.write(data)
					if len(data) == packetSize:
						data, serverAddress = clientSocket.recvfrom(packetSize)
					else:
						data = bytes()
					print(" recibiendo... %s" %len(data))
					
			except IOError:
				print("File requested not found")
			except timeout:
				print("timeout")
			finally:
				try:
					f.close()
					clientSocket.close()
				except:
					pass
		else:
			print("Error len del comando")
	else:
		print("Error no es put")
else:
	print("Error no hay mensaje")
# Print the converted text and then close the socket
#print (modifiedMessage.decode())
clientSocket.close()
print("Se acaba")
