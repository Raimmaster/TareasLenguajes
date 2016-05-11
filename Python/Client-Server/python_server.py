import time
import UsersManager
import FileManager
import os.path
from socket import *


fManager = FileManager.FileManager("usuarios.txt")
users = []
if (os.path.isfile(fManager.usersFile)):
	users = fManager.toUserList(fManager.readFile())

print (users)

#para el socket
server_socket = socket(AF_INET, SOCK_STREAM) #Crear socket TCP
server_socket.bind(('', 8888)) #bind to port 8888
server_socket.listen(5) #5 conexiones pendientes

while True:
	client_socket, addr = server_socket.accept() #get connection
	print("Obtuve conexion de dir %s" % str(addr))
	timestr = time.ctime(time.time()) + "\r\n"
	client_socket.send(timestr.encode('ascii'))
	client_socket.close()

server_socket.close();


def createConnection():
	#crear/aceptar conexión para el usuario
	return

def closeConnection(): #exit?
	#logging out, cerrar conexión para el usuario
	return

def changeDirectory(): #cd
	return

def listFiles(): #ls
	return

def putFile(): #get file from client, save in server
	return

def getFile(): #give file to client
	return

def removeFile(): #remove file or directory
	return

def createDirectory(): #mkdir
	return

def getCurrentDirName(): #pwd, optional
	return

def exit(): #close server?
	return