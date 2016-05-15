import UsersManager
import FileManager
import LoggedUser
import time
import os
from socket import *

def createConnection():
	#crear aceptar conexion para el usuario
	return

def closeConnection(): #exit?
	#logging out, cerrar conexion para el usuario
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
op_con_dirs = (1, 5, 6, 7)

while option_received != 3: #3 salir
	try:		
		client_socket, addr = server_socket.accept() #get connection
		print("Obtuve conexion de dir %s" % str(addr))	
		option_received = int(str(client_socket.recv(1024), ('ascii')))
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
				dir_name = ''
				file_name = ''
				while (True):
					if mensaje_enviar == 'Written':
						#print("Rebooting connection!")
						client_socket.close()
						client_socket, addr = server_socket.accept()

					option_received = int(str(client_socket.recv(1024).decode('ascii')))

					if(option_received in op_con_dirs):
						dir_name = str(client_socket.recv(1024).decode('ascii'))
					
					if(option_received == 3 or option_received == 4):
						print("Opcion: " + str(option_received))
						file_name = str(client_socket.recv(1024).decode('ascii'))

					if(option_received == 1):#cd
						loggedUser.changeDirectory(dir_name)
						mensaje_enviar = 'cd'
					elif(option_received == 2): #ls
						loggedUser.listFiles()
						mensaje_enviar = 'ls' 
					elif(option_received == 3): #put
						dir_to_write = loggedUser.getCurrentDirName()

						while True:
							path_write = dir_to_write + '/' + file_name
							print(path_write)
							n_file = open(path_write, 'wb')
							while(not n_file.closed):
								#recibimos y escribimos
								data = client_socket.recv(1024)
								while(data):
									n_file.write(data)
									data = client_socket.recv(1024)
								n_file.close()									
							break

						mensaje_enviar = 'Written'
						loggedUser.putFile(dir_name)
					elif(option_received == 4): #get		
						loggedUser.getFile(dir_name)
						mensaje_enviar = 'get'
					elif(option_received == 5): #rm file
						loggedUser.removeFile(dir_name)
						mensaje_enviar = 'rm'
					elif(option_received == 6): #rmdir
						loggedUser.removeDirectory(dir_name)
						mensaje_enviar = 'rmdir'
					elif(option_received == 7): #mkdir			
						loggedUser.createDirectory(dir_name)
						mensaje_enviar = 'mkdir'
					elif(option_received == 8): #pwd
						estoy = loggedUser.getCurrentDirName()
						#print(estoy)
						mensaje_enviar = 'pwd'
						client_socket.sendall(estoy.encode('ascii'))
						time.sleep(0.3)
					elif(option_received == 9): #exit
						print('Logging user off...')	
						mensaje_enviar = 'Log Off:'
					
					client_socket.sendall(mensaje_enviar.encode('ascii'))	

					if(option_received == 9):
						break							
	finally:			
		print('Ha acabado.')
		client_socket.close()

exit()	
server_socket.close()
client_socket.close()
print('Adios')