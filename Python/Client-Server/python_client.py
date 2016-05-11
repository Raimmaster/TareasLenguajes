#time client program
from socket import *

#tm = client_socket.recv(1024) #recibir no más de 1 KB

#print("El tiempo es %s" % tm.decode('ascii'))
#salir_op = input("Salir? Y/N ")

#if(salir_op == "Y"):
#	client_socket.close()

opcion = 0

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
			print('')
		finally:
			op = 0

	elif (opcion == 3):
		try:
			client_socket = socket(AF_INET, SOCK_STREAM) #crear TCP socket
			client_socket.connect(('localhost', 8888)) #conectar al servidor

			client_socket.sendall(str(opcion).encode('ascii'))
			
		finally:
			client_socket.close()
		print("Saliendo...")
