import os

class LoggedUser:

	def __init__(self, username):
		self.username = username
		self.current_dir = 'Usuarios/' + username
		#crear carpeta personal si no existe
		if(not os.path.isdir(self.current_dir)):
				os.mkdir(dirName)
		self.prev_dir = self.current_dir
		self.logged = True

	def changeDirectory(self, new_dir): #cd
		own_dir = 'Usuarios/' + username
		if (new_dir == own_dir):
			print('Ya se encuentra en este directorio.')
		elif(new_dir == '..'):
			self.current_dir = self.prev_dir
			self.prev_dir = self.current_dir
			return self.current_dir
		else:
			files_dirs = os.listdir()
			if(new_dir in files_dirs and os.path.isdir(new_dir)):
				self.prev_dir = self.current_dir
				self.current_dir = self.prev_dir + "/" + new_dir

	def listFiles(self): #ls		
		for file in os.listdir():
			if(os.path.isdir(file)):
				print ("* %s " % file)
			else:		
				print ("- %s " % file)

	def putFile(self, filename): #get file from client, save in server
		return

	def getFile(self, filename): #give file to client
		return

	def removeFile(self, filename): #remove file
		os.remove(filename)
		return

	def removeDirectory(self, dirname, username): #remove directory and all its files
		path = self.current_dir + "/" + dirname + "/"
		files = os.listdir(path)
		for f in files:
			removeFile(f)

		os.rmdir(dirName)

		return

	def createDirectory(self, dirName): #mkdir
		dirFullPath = self.current_dir + "/" + dirName
		if(not os.path.isdir(dirFullPath)):
			os.mkdir(dirFullPath)
			return True

		return False

	def getCurrentDirName(self): #pwd, optional
		return self.current_dir

	def exit(): #close server?
		return	