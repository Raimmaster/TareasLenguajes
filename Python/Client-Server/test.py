import FileManager
import User
import os

fTester = FileManager.FileManager("usuarios.txt")

#fTester.writeToFile()
lista = fTester.readFile()
userList = []

for u in lista:
	usuario = User.User(str(u.get('username')), str(u.get('password')))
	userList.append(usuario)

for u in userList:
	print(u.username + ' ' + u.password)
	dirName = "Usuarios/" + u.username 
	if(not os.path.isdir(dirName)):
		os.mkdir(dirName)
		print("Created!")
