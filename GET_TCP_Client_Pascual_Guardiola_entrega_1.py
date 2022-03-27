from ast import While
from http import client
import sys
from socket import *


print("##############################################")
print("#####                                    #####")
print("#####          TCP CLIENT - GET          #####")
print("#####          Alex P. y Gabriel         #####")
print("#####                v1.0                #####")
print("#####                                    #####")
print("##############################################")


method = "GET"

serverName = '192.168.1.200'
serverPort = 12004
packetSize = 1024
# Request IPv4 and TCP communication

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

    #concatena el metodo (GET) con el archivo
    client_msg = method + " " + filename
    #envia el comando + el archivo al servidor
    clientSocket.send(client_msg.encode())
    #el cliente espera a recibir si ha habido algun error
    fileExistsChecker = clientSocket.recv(packetSize).decode()
    #printa el estado
    print(fileExistsChecker)

    #si lo ha encontrado, recoge el tamaño del archivo para informar del estado de la descarga

    if "encontrado" in fileExistsChecker:
        totalSize = fileExistsChecker.split("|");totalSize = totalSize[3]

    else:
        return 0
        
    #recibe el primer paquete del archivo
    fileFromServer = clientSocket.recv(packetSize)
    #packetsRecv guarda la cantidad de bytes que se han descargado del archivo
    packetsRecv = len(fileFromServer)
    #DEBUG - para comprobar la descarga en localhost
    #filename = "test.txt"
    #crea el fichero en local

    try:
        f = open(filename, "wb")
    except FileNotFoundError:
        print("ERROR - No es posible crear el archivo, has puesto una ruta, crea el directorio antes.")
        return 0
    #mientras la longitud de los datos recibidos sean mayores que cero, sigue recibiendo
    while len(fileFromServer) > 0:
        #escribe el paquete de datos en el archivo local
        f.write(fileFromServer)
        #recibe el siguiente paquete
        fileFromServer = clientSocket.recv(packetSize)
        #informa de el proceso de descarga
        percent = round(((packetsRecv/int(totalSize))*100),2)
        print("Descargando [{}] {}/{} (bytes) - {}%".format(filename,packetsRecv,totalSize,percent))
        #suma el siguiente paquete en bytes al total
        packetsRecv += len(fileFromServer)
        #si la longitud del ultimo recibido es cero, ya no hay más paquetes
        #informa, cierra el fd y el socket
        if len(fileFromServer) == 0:
            print("{} DESCARGADO CON ÉXITO.".format(filename))
            fileFromServer = bytes()

    f.close()

    clientSocket.close()

while True:

    clientSocket = socket(AF_INET, SOCK_STREAM)
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
