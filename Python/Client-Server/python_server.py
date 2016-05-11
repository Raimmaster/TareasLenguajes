import UsersManager
import FileManager
import LoggedUser
import os
from socket import *


def createConnection():
	#crear/aceptar conexión para el usuario
	return

def closeConnection(): #exit?
	#logging out, cerrar conexión para el usuario
	return

def exit(): #close server?
	client_socket.close();
	fManager.writeToUsersFile(userManager.listOfUsers)
	print ("Conexion cerrada de: %s" % str(addr))	
	return

#Check on users, create otherwise
if(not os.path.isdir('Usuarios')):
	os.mkdir('Usuarios')
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
				print('Logineado')
				loggedUser = LoggedUser.LoggedUser(username)
				client_socket.sendall(mensaje_enviar.encode('ascii'))
				while (True):
					opciones = (1, 2, 3, 4, 5, 6 ,7)			
	finally:			
		print('Ha acabado.')

exit()	
server_socket.close()
print('Adios')