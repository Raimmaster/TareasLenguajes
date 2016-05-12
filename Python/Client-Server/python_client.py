#!/usr/bin/env python

# -*- coding: utf-8 -*-

#

#time client program
from socket import *
#import socket
#tm = client_socket.recv(1024) #recibir no más de 1 KB

#print("El tiempo es %s" % tm.decode('ascii'))
#salir_op = input("Salir? Y/N ")

#if(salir_op == "Y"):
#	client_socket.close()

opcion = 0
logged_options = ('1. cd', '2. ls', '3. put (file)', '4. get', '5. rm file', '6. rmdir dir', '7. mkdir dir', '8. pwd', '9. Salir')
while (opcion != 3):
	print('')
	print("1. Crear usuario. ")
	print("2. Login. ")
	print("3. Salir. ")
	opcion = int(input("Escribir opcion: "))

	if (opcion == 1):
		try:
			#conectar
			client_socket = socket(AF_INET, SOCK_STREAM) #crear TCP socket
			client_socket.connect(('localhost', 8888)) #conectar al servidor

			client_socket.sendall(str(opcion).encode('ascii'))
			#response_received = str(client_socket.recv(1024),'utf-8')

			print("File descriptor: ", client_socket.fileno())
			print("Remote address: ", client_socket.getpeername())
			print("My address: ", client_socket.getsockname())

			while True:
				#print("Dude!")
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
						op = 0 
						break
								
		finally:
			client_socket.close()

	elif (opcion == 2):
		try:
			#conectar
			client_socket = socket(AF_INET, SOCK_STREAM) #crear TCP socket
			client_socket.connect(('localhost', 8888)) #conectar al servidor

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
							dir_name = input('Ingrese el nombre del archivo a bajar: ')
							file_name = input('Ingrese el nombre del nuevo archivo: ')
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
							break

						client_socket.sendall(str(selected_option).encode('ascii'))
						if(selected_option in op_con_dirs):
							client_socket.sendall(dir_name.encode('ascii'))

						if(selected_option == 3):
							client_socket.sendall(((file_name)).encode('utf-8'))
							f_send = open (dir_name, "rb") 
							bytes_data = f_send.read(1024)
							while (bytes_data):
							    client_socket.sendall(bytes_data)
							    bytes_data = f_send.read(1024)

							f_send.close()
							print('Archivo enviado')
							#client_socket.shutdown(socket.SHUT_WR)
							client_socket.close()
							op = 0

						data_con = client_socket.recv(1024)
						print(str(data_con.decode('ascii')))
		finally:
			client_socket.close()
	elif (opcion == 3):
		try:
			client_socket = socket(AF_INET, SOCK_STREAM) #crear TCP socket
			client_socket.connect(('localhost', 8888)) #conectar al servidor

			client_socket.sendall(str(opcion).encode('ascii'))
			
		finally:
			client_socket.close()
		print("Saliendo...")
