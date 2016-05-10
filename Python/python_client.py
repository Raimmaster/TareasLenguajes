#time client program
from socket import *

s = socket(AF_INET, SOCK_STREAM) #crear TCP socket
s.connect_ex(('localhost', 8888)) #conectar al servidor
tm = s.recv(1024) #recibir no más de 1 KB
print("File descriptor: ", s.fileno())
print("Remote address: ", s.getpeername())
print("My address: ", s.getsockname())

print("El tiempo es %s" % tm.decode('ascii'))
salir_op = input("Salir? Y/N ")

if(salir_op == "Y"):
	s.close()