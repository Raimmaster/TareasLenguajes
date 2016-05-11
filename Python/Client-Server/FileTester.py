import User
import json
import os.path

class FileTester:

	def __init__(self, usersFile):
		self.usersFile = usersFile
		self.usuariosList = []

	def writeToFile(self, userList):		
		if(os.path.isfile(self.usersFile)):
			#salvar la lista anterior de usuarios, y sobreescribir
			self.readFile()

		#usuario = User.User('Yo', 'Daa')				
		#usuario2 = User.User('Doo', 'Dee')
		#userList = []
		#self.usuariosList.append(usuario)
		#self.usuariosList.append(usuario2)
		#userList = {usuario.userToList(), usuario2.userToList()}
		with open(self.usersFile, "w") as file:
			json.dump(self.usuariosList, file, default=lambda userDict: userDict.__dict__)

	def readFile(self):
		with open(self.usersFile, 'r+') as file:
			self.usuariosList = (json.load(file))

		return self.usuariosList
			#print current users
		#print(self.usuariosList)

	def toUserList(self, lista):
		userList = []
		for u in lista:
			usuario = User.User(str(u.get('username')), str(u.get('password')))
			userList.append(usuario)

		return userList