import User

class UsersManager:

	def __init__(self, lista):
		self.listOfUsers = lista

	def createUser(self, username, password):
		user = User.User(username, password)
		self.listOfUsers.append(user)

		for us in self.listOfUsers:
			print(us.username)
		#code for creating

	def findUser(self, username):
		#for finding if username already exists
		for u in self.listOfUsers:
			if (u.username == username):
				return u

		return None

	def login(self, username, password):
		#to create a connection with the sockets
		user = findUser()
		if(user):
			if(user.password == password):
				return True
		
		return False


	#yet to be implemented
	def findActiveUser(self, username):
		#find if user is already logged on, limiting another connection from it
		return
		
	def logout(self, username):
		#log out the user and mark as inactive
		return (username, True)

	def loadUsers(self):
		#loading from files
		return

	def printUsers(self):
		#show active users
		return

	#def deleteUser(username): optional