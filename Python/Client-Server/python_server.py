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

op = 0

while op != 3: #3 salir
	try:
		client_socket, addr = server_socket.accept() #get connection
		print("Obtuve conexion de dir %s" % str(addr))
		#timestr = time.ctime(time.time()) + "\r\n"
		#client_socket.send(timestr.encode('ascii'))
		#client_socket.close()
		option_received = int(str(client_socket.recv(1024), 'ascii'))
		if(option_received == 1):
			#print("Ing")
			mensaje_enviar = 'Ingresar usuario:'
			client_socket.sendall(mensaje_enviar.encode('ascii'))
			#print("aspetto")
			username = str(client_socket.recv(1024).decode('ascii'))		
			password = str(client_socket.recv(1024).decode('ascii'))
			#print("pasado")
			userManager.createUser(username, password)		
			mensaje_enviar = 'Usuario creado'
			client_socket.sendall(mensaje_enviar.encode('ascii'))
			print ("Creado")
	finally:		
		client_socket.close();
		print ("Con closed")


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