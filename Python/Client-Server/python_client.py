import time
import sys
import os
from socket import *

#update buffer in Python3
if sys.version_info > (3,):
	buffer = memoryview

def put(client_socket, file_name, dir_name): #send files
	time.sleep(0.3)
	#file info
	file_name = buffer(file_name.encode())
	file_info = os.stat(dir_name)
	file_size = file_info.st_size
	#send file and its size
	client_socket.sendall(file_name)
	time.sleep(0.2)
	client_socket.send(str(file_size).encode('ascii'))
	#open file	
	f_send = open (dir_name, "rb") 
	time.sleep(0.2)
	bytes_data = f_send.read(1024)
	while (bytes_data):
		client_socket.sendall(bytes_data)
		bytes_data = f_send.read(1024)

	f_send.close()
	print('Archivo enviado')
	
def get(client_socket, file_path, file_name): #get files
	client_socket.sendall(file_name.encode('ascii'))
	#get the size to be reading
	file_size = int(str(client_socket.recv(1024).decode('ascii')))
	reading_size = 1024
	size_read = 0	

	path_write = file_path + '/' + file_name
	n_file = open(path_write, 'wb')
	while(not n_file.closed):
		#recibimos y escribimos
		if(file_size < reading_size):
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
	
opcion = 0
logged_options = ('1. cd', '2. ls', '3. put (file)', '4. get', '5. rm file', '6. rmdir dir', '7. mkdir dir', '8. pwd', '9. Salir')
#connect to server
client_socket = socket(AF_INET, SOCK_STREAM) #crear TCP socket
client_socket.connect(('localhost', 8888)) #conectar al servidor

while (opcion != 3):
	print('')
	print("1. Crear usuario. ")
	print("2. Login. ")
	print("3. Salir. ")
	opcion = int(input("Escribir opcion: "))

	if (opcion == 1):
		try:
			client_socket.sendall(str(opcion).encode('ascii'))

			while True:
				response = client_socket.recv(1024)
				print(response.decode('ascii'))
				if response.decode('ascii') =='Ingresar usuario:':
					username = input("Ingrese el username: ")
					password = input("Ingrese el password: ")
					#send to server for creation
					client_socket.sendall(username.encode('ascii'))							
					client_socket.sendall(password.encode('ascii'))
					mensaje = client_socket.recv(1024)
					if (mensaje.decode('ascii') == 'Usuario creado'):
						print ("Perfect!")
						break
		finally:
			print('')

	elif (opcion == 2):
		try:
			client_socket.sendall(str(opcion).encode('ascii'))
			response = client_socket.recv(1024)
			print(response.decode('ascii'))
		
			if response.decode('ascii') =='Login:':
				username = input("Ingrese el user: ")
				password = input("Ingrese el pass: ")
				#send to server for creation
				client_socket.sendall(username.encode('ascii'))							
				client_socket.sendall(password.encode('ascii'))
				mensaje = client_socket.recv(1024)

				if (mensaje.decode('ascii') == 'Dir User:'):#conectado
					print ("Conexion establecida!")		

					data_con = ''
					op_con_dirs = (1, 5, 6, 7)
					while data_con != 'Log Off:':

						print('Opciones: \n')
						for indices in logged_options:
							print(indices)
						
						selected_option = int(input('Elegir: '))
						dir_name = ''
						
						if(selected_option == 1): #cd
							dir_name = input('Ingrese el nuevo directorio a estar: ')
						elif(selected_option == 2): #ls
							print('Listar directorios: \n')
						elif(selected_option == 3): #put
							dir_name = input('Ingrese el path del archivo a subir: ')
							file_name = input('Nombre de nuevo archivo: ')
						elif(selected_option == 4): #get						
 							file_name = input('Ingrese el nombre del nuevo archivo: ')
 							file_path = input('Ingrese el path donde estara: ')
						elif(selected_option == 5): #rm file						
							dir_name = input('Ingrese el nombre del archivo a eliminar: ')
						elif(selected_option == 6): #rmdir
							dir_name = input('Ingrese el nombre del directorio a eliminar: ')
						elif(selected_option == 7): #mkdir							
							dir_name = input('Ingrese el path del directorio a crear: ')
						elif(selected_option == 8): #pwd
							print('Me encuentro en: ')
						elif(selected_option == 9): #exit
							print('Log off...')

						client_socket.sendall(str(selected_option).encode('ascii'))
						if(selected_option in op_con_dirs):
							client_socket.sendall(dir_name.encode('ascii'))

						if(selected_option == 2):
							files_list = str(client_socket.recv(1024).decode('ascii'))
							print(files_list)
						#code for sending files 
						elif(selected_option == 3):
							put(client_socket, file_name, dir_name)

						#code for reading files
						elif(selected_option == 4): #get
							get(client_socket, file_path, file_name)

						elif(selected_option == 8):#receive pwd
							print(str(client_socket.recv(1024).decode('ascii')))

						#read the final message
						if (selected_option != 4):
							data_con = str(client_socket.recv(1024).decode('ascii'))
						else:
							data_con = 'Sent'
						print(data_con)							
		finally:
			print('')
	elif (opcion == 3):
		client_socket.close()
		print("Saliendo...")
