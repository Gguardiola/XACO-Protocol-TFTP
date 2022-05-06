from ast import While
from http import client
import sys
from socket import *
import os


print("##############################################")
print("#####                                    #####")
print("#####          TCP CLIENT - PUT          #####")
print("#####          Alex P. y Gabriel         #####")
print("#####                v2.0                #####")
print("#####                                    #####")
print("##############################################")


method = "PUT"

serverName = 'localhost'
serverPort = 12004
packetSize = 1024
packetSizeOpt = [32,64,128,256,512,1024,2048]

def startClient(packetSize):
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

        clientSocket.send("encontrado |{}".format(totalSize).encode())
    except FileNotFoundError:
        print("No se encuentra el fichero!")
        clientSocket.close()
        return 0

    #establecer el tamaño del paquete
    newSize = 0
    while newSize not in packetSizeOpt:
        try:
            newSize = int(input("Tamaño del paquete: "))
            if newSize not in packetSizeOpt:
                print("ERROR - Introduce un valor entre 32 y 2048.")
        except AttributeError:
            print("ERROR - Introduce un valor numerico.")
    newSize = str(newSize)
    packetSize = int(newSize)
    #envia el tamaño del paquete
    clientSocket.send(newSize.encode())
    print("Tamaño del paquete establecido en " + newSize + " bytes.")
    #packetsSended guarda el avance del envio del archivo
    #recibe el primer paquete del archivo
    file = f.read(packetSize)
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
        startClient(packetSize)
    except ConnectionResetError as e:
        print(e)
        sys.exit()
