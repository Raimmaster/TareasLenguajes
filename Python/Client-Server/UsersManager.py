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
		user = self.findUser(username)
		if(user):
			print('Found user')
			if(user.password == password):
				return True
		
		return False