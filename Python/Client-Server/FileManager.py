import os
import User
import json

class FileManager:

	def __init__(self, usersFile):
		self.usersFile = usersFile
		self.usuariosList = []

	def writeToUsersFile(self, userList):		
		if(os.path.isfile(self.usersFile)):
			#salvar la lista anterior de usuarios, y sobreescribir
			self.readUsersFile()

		with open(self.usersFile, "w") as file:
			json.dump(userList, file, default=lambda userDict: userDict.__dict__)

	def readUsersFile(self):
		with open(self.usersFile, 'r+') as file:
			self.usuariosList = (json.load(file))

		return self.usuariosList

	def toUserList(self, lista):
		userList = []
		for u in lista:
			usuario = User.User(str(u.get('username')), str(u.get('password')))
			userList.append(usuario)
			#crear directorio en caso que no exista
			dirName = "Usuarios/" + usuario.username 
			if(not os.path.isdir(dirName)):
				os.mkdir(dirName)
				print("Created user dir!")

		return userList