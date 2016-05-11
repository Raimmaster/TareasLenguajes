#time client program
from socket import *

#tm = client_socket.recv(1024) #recibir no más de 1 KB

#print("El tiempo es %s" % tm.decode('ascii'))
#salir_op = input("Salir? Y/N ")

#if(salir_op == "Y"):
#	client_socket.close()

opcion = 0
logged_options = ('1. cd', '2. ls', '3. put (file)', '4. get', '5. rm file', '6. rmdir dir', '7. mkdir dir', '8. pwd')
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
					print('Opciones: \n')
					for indices in logged_options:
						print(indices)
					data_con = ''
					while data_con != 'Log Off:':
						print('')
			
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
