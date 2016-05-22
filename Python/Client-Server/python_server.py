import UsersManager
import FileManager
import LoggedUser
import time
import os
from _thread import *	
from socket import *

def createConnection():
	#crear aceptar conexion para el usuario
	return

def closeConnection(): #exit?
	#logging out, cerrar conexion para el usuario
	return

def exit(): #close server
	fManager.writeToUsersFile(userManager.listOfUsers)
#	print ("Conexion cerrada de: %s" % str(addr))	
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

def client_thread(client_socket, addr):
#infinite loop so that function do not terminate and thread do not end.
	while True:
		option_received = 0
		op_con_dirs = (1, 5, 6, 7)

		while option_received != 3: #3 salir
			try:		
				#client_socket, addr = server_socket.accept() #get connection
				#start_new_thread(client_thread, (client_socket,))
				print("Obtuve conexion de dir %s" % str(addr))	
				option_received = int(str(client_socket.recv(1024), ('ascii')))
				if(option_received == 1): #para ingresar usuario
					mensaje_enviar = 'Ingresar usuario:'
					client_socket.sendall(mensaje_enviar.encode('ascii'))			
					username = str(client_socket.recv(1024).decode('ascii'))		
					password = str(client_socket.recv(1024).decode('ascii'))
					userManager.createUser(username, password)		
					mensaje_enviar = 'Usuario creado'
					exit() #escribir usuario
					client_socket.sendall(mensaje_enviar.encode('ascii'))
					#client_socket.exit()
					print ("Creado")
				elif(option_received == 2):
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
							#if mensaje_enviar == 'Written' or mensaje_enviar == 'Sent':
							#	client_socket.close()
							#	client_socket, addr = server_socket.accept()

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
								files_list = loggedUser.listFiles()
								mensaje_enviar = 'ls' 
								client_socket.sendall(files_list.encode('ascii'))
								time.sleep(0.3)
							elif(option_received == 3): #put
								dir_to_write = loggedUser.getCurrentDirName()
								file_size = int(str(client_socket.recv(1024).decode('ascii')))								
								reading_size = 1024
								size_read = 0
								while True:
									path_write = dir_to_write + '/' + file_name
									n_file = open(path_write, 'wb')
									while(not n_file.closed):
										#recibimos y escribimos
										if (file_size < reading_size):
											cant_read = file_size 
										else:
											cant_read = reading_size													
										data = client_socket.recv(cant_read)
										size_read = len(data)
										while(data):
											n_file.write(data)
											cant_read = min(file_size - size_read, reading_size)										
											if(cant_read == 0):
												break
											data = client_socket.recv(cant_read)
											size_read = size_read + len(data)
										n_file.close()									
									break

								mensaje_enviar = 'Written'
								print('Obtenido archivo')
							elif(option_received == 4): #get		
								file_dir = loggedUser.getCurrentDirName()
								#file_name = str(client_socket.recv(1024).decode('ascii'))
								file_path = file_dir + '/' + file_name
								file_info = os.stat(file_path)
								file_size = file_info.st_size
								time.sleep(0.1)
								client_socket.send(str(file_size).encode('ascii'))								
								time.sleep(0.3)

								f_send = open (file_path, "rb") 
								bytes_data = f_send.read(1024)
								while (bytes_data):
								    client_socket.sendall(bytes_data)
								    bytes_data = f_send.read(1024)

								f_send.close()
								print('Archivo enviado')
								#client_socket.close()

								mensaje_enviar = 'Sent'
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
								mensaje_enviar = 'pwd'
								client_socket.sendall(estoy.encode('ascii'))
								time.sleep(0.3)
							elif(option_received == 9): #exit
								print('Logging user off...')	
								mensaje_enviar = 'Log Off:'
							
							if(option_received != 4):
								client_socket.sendall(mensaje_enviar.encode('ascii'))	

							if(option_received == 9):
								break							
			finally:			
				print('Ha acabado.')
				#client_socket.close()

		exit()	
		#server_socket.close()
		client_socket.close()
		print('Adios')
		break

while True:
	cliente_socket, addre = server_socket.accept() #get connection
	start_new_thread(client_thread, (cliente_socket, addre))
	#print("Obtuve conexion de dir %s" % str(addre))	
		
