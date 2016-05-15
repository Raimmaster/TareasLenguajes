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
		own_dir = 'Usuarios/' + self.username
		print ('new dir: %s' % new_dir )
		if (new_dir == own_dir):
			print('Ya se encuentra en este directorio.')
		elif(new_dir == '..'):
			self.current_dir = self.prev_dir
			self.prev_dir = self.current_dir
			return self.current_dir
		else:
			files_dirs = os.listdir(self.current_dir)
			el_dir = self.current_dir + '/' + new_dir
			if(new_dir in files_dirs and os.path.isdir(el_dir)):
				self.prev_dir = self.current_dir
				self.current_dir = self.prev_dir + "/" + new_dir

    #sb = []
    #for i in range(30):
    #    sb.append("abcdefg"[i%7])

    #return ''.join(sb)

	def listFiles(self): #ls		
		f_names = []
		for file in os.listdir(self.current_dir):
			if(os.path.isdir(self.current_dir + '/' + file)):
				f_names.append('*: ' + file + "\n")
				print ("* %s " % file)
			else:		
				f_names.append(file + "\n")
				print ("- %s " % file)

		return ''.join(f_names)

	def putFile(self, filename): #get file from client, save in server
		return

	def getFile(self, filename): #give file to client
		return

	def removeFile(self, filename): #remove file
		file_to_remove = self.current_dir + '/' + filename
		os.remove(file_to_remove)
		return

	def removeDirectory(self, dirname): #remove directory and all its files
		path = self.current_dir + "/" + dirname + "/"
		files = os.listdir(path)
		path_prefix = self.current_dir + '/' + dirname + '/'
		for f in files:
			os.remove(path_prefix + f)

		os.rmdir(path_prefix)

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