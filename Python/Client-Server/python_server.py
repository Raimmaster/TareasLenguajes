#time server program
from socket import *
import time
import UsersManager



s = socket(AF_INET, SOCK_STREAM) #Crear socket TCP
s.bind(('', 8888)) #bind to port 8888
s.listen(5) #5 conexiones pendientes

while True:
	client_socket, addr = s.accept() #get connection
	print("Obtuve conexion de dir %s" % str(addr))
	timestr = time.ctime(time.time()) + "\r\n"
	client_socket.send(timestr.encode('ascii'))
	client_socket.close()

s.close();

def createConnection():
	#crear/aceptar conexión para el usuario

def closeConnection(): #exit?
	#logging out, cerrar conexión para el usuario

def changeDirectory(): #cd

def listFiles(): #ls

def putFile(): #get file from client, save in server

def getFile(): #give file to client

def removeFile(): #remove file or directory

def createDirectory(): #mkdir

def getCurrentDirName(): #pwd, optional

def exit(): #close server?