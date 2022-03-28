# Example UDP socket client that fires some text at a server

from socket import *

# Default to running on localhost, port 12000
serverName = 'localhost'
serverPort = 12000
size = 512
# Request IPv4 and UDP communication
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Read in some text from the user
message = input('Escriu command:')
command = message.split()
if len(command) > 0:
	if command[0] == 'put':
		if len(command) == 2 or len(command) == 3:
			#enviamos el comando con el fichero que vamos a subir
			clientSocket.sendto(message.encode(),(serverName,serverPort))
			try:
				# TODO: if file not exists, what happends with the client
				f = open(command[1], "rb")
				archive = f.read(size)
				print("enviando... %s" %len(archive))
				while (len(archive) > 0):
					if (clientSocket.sendto(archive, (serverName, serverPort))):
						if(len(archive) == size):
							archive = f.read(size)
							if (len(archive) == 0): # Si es un fichero multiplo de size enviamos un paquete con 0 bytes de datos para comunicar al cliente que hemos acabado
								clientSocket.sendto(archive, (serverName, serverPort))
						else:
							archive = bytes()
						print("enviando... %s" %len(archive))
			except IOError as e:
				print("File requested not found")
				print(e)
			finally:
				try:
					f.close()
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
