import time
import UsersManager
import FileManager
import os
from socket import *

#Check on users, create otherwise
fManager = FileManager.FileManager("usuarios.txt")
users = []
if (os.path.isfile(fManager.usersFile)):
	users = fManager.toUserList(fManager.readUsersFile())

userManager = UsersManager.UsersManager(users)

#para el socket
server_socket = socket(AF_INET, SOCK_STREAM) #Crear socket TCP
server_socket.bind(('', 8888)) #bind to port 8888
server_socket.listen(5) #5 conexiones pendientes

option_received = 0

while option_received != 3: #3 salir
	try:
		client_socket, addr = server_socket.accept() #get connection
		print("Obtuve conexion de dir %s" % str(addr))	
		option_received = int(str(client_socket.recv(1024), 'ascii'))
		if(option_received == 1): #para ingresar usuario
			mensaje_enviar = 'Ingresar usuario:'
			client_socket.sendall(mensaje_enviar.encode('ascii'))			
			username = str(client_socket.recv(1024).decode('ascii'))		
			password = str(client_socket.recv(1024).decode('ascii'))			
			userManager.createUser(username, password)		
			mensaje_enviar = 'Usuario creado'
			client_socket.sendall(mensaje_enviar.encode('ascii'))
			print ("Creado")
		if(option_received == 2):
			mensaje_enviar = 'Login:'
			client_socket.sendall(mensaje_enviar.encode('ascii'))			
			username = str(client_socket.recv(1024).decode('ascii'))		
			password = str(client_socket.recv(1024).decode('ascii'))						
			if(userManager.login(username, password)): #permitir las otras funciones
				mensaje_enviar = 'Dir User:'
				client_socket.sendall(mensaje_enviar.encode('ascii'))
				while (True):
					print('el resto')
	finally:		
		client_socket.close();
		fManager.writeToUsersFile(userManager.listOfUsers)
		print ("Conexion cerrada de: %s" % str(addr))

server_socket.close()

def createConnection():
	#crear/aceptar conexión para el usuario
	return

def closeConnection(): #exit?
	#logging out, cerrar conexión para el usuario
	return

def changeDirectory(): #cd
	return

def listFiles(): #ls
	for file in os.listdir():
		if(os.path.isdir(file)):
			print ("* %s " % file)
		else:		
			print ("- %s " % file)
	

def putFile(): #get file from client, save in server
	return

def getFile(): #give file to client
	return

def removeFile(filename): #remove file
	os.remove(filename)
	return

def removeDirectory(dirname, username): #remove directory and all its files
	path = "Usuarios/" + username + "/" + dirname + "/"
	files = os.listdir(path)
	for f in files:
		removeFile(f)

	os.rmdir(dirName)

	return

def createDirectory(username, dirName): #mkdir
	dirFullPath = "Usuarios/" + username + "/" + dirName
	if(not os.path.isdir(dirFullPath)):
		os.mkdir(dirFullPath)
		return True

	return False

def getCurrentDirName(): #pwd, optional
	return

def exit(): #close server?
	return