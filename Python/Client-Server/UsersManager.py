import User

class UsersManager:

	def __init__(self, lista):
		self.listOfUsers = lista

	def createUser(self):
		username = input("Ingrese el username: ")
		password = input("Ingrese el password: ")
		user = User.User(username, password)
		self.listOfUsers.append(user)
		#code for creating

	def findUser(self, username):
		#for finding if username already exists
		for u in self.listOfUsers:
			if (u.username == username)
				return u

		return False

	def login(self, username, password):
		#to create a connection with the sockets
		user = findUser()
		if(user)
			if(user.password == password)
				return True
		
		return False


	#yet to be implemented
	def findActiveUser(self, username):
		#find if user is already logged on, limiting another connection from it
		return
		
	def logout(self, username):
		#log out the user and mark as inactive
		return

	def loadUsers(self):
		#loading from files
		return

	def printUsers(self):
		#show active users
		return

	#def deleteUser(username): optional