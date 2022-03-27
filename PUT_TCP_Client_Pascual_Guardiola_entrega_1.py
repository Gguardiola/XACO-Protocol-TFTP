from ast import While
from http import client
import sys
from socket import *
import os


print("##############################################")
print("#####                                    #####")
print("#####          TCP CLIENT - PUT          #####")
print("#####          Alex P. y Gabriel         #####")
print("#####                v1.0                #####")
print("#####                                    #####")
print("##############################################")


method = "PUT"

serverName = '192.168.1.200'
serverPort = 12004
packetSize = 1024

def startClient():
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
    try:
        f = open(filename,"rb")
        #lee los n primeros bytes -> Va leyendo el archivo segmentado para enviarlo en paquetes al servidor
        file = f.read(packetSize)
        #recoge la mida total para informar cuanto queda por enviar
        totalSize = os.path.getsize(filename)
        #informa al cliente de que el se ha encontrado.
        #de paso le envia la mida total del archivo
        comando = method + " " + filename
        clientSocket.send(comando.encode())
        statusChecker = clientSocket.recv(packetSize).decode()
        print(statusChecker)
        if "no compatible" in statusChecker:
            clientSocket.close()
            return 0

        clientSocket.send("Fichero: |{}| Peso: |{}| encontrado, enviando...".format(filename,totalSize).encode())
    except FileNotFoundError:
        print("No se encuentra el fichero!")
        clientSocket.close()
        return 0

    #packetsSended guarda el avance del envio del archivo
    packetsSended = len(file)

    while len(file) > 0:
        percent = round(((packetsSended/int(totalSize))*100),2)
        print("Enviando [{}] {}/{} (bytes) - {}%".format(filename,packetsSended,totalSize,percent))
        #envia el paquete
        clientSocket.send(file)
        #lee los siguientes n bytes del paquete
        file = f.read(packetSize)
        #aumenta la cantidad de bytes enviados
        packetsSended += len(file)
        #si el la longitud del fichero es cero, signfiica que ya ha enviado todo. Envia byte de finalización
        if len(file) == 0:
            print("ENVIADO CON EXITO A {}".format(serverName))
            clientSocket.send(bytes())	

    f.close()
    clientSocket.close()
    sys.exit()

while True:
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Open the TCP connection to the server at the specified port 
    try:
        clientSocket.connect((serverName,serverPort))
        print("CONEXIÓN ESTABLECIDA!")
        print("Servidor: {} | Puerto: {}\n".format(serverName,serverPort))
    except ConnectionRefusedError as e:
        print(e,"- No se encuentra el servidor.")
        sys.exit()
    except TimeoutError as e:
        print(e)
        sys.exit()
        
    try:
        startClient()
    except ConnectionResetError as e:
        print(e)
        sys.exit()
