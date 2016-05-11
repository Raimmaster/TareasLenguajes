import FileTester
import User
fTester = FileTester.FileTester("usuarios.txt")

#fTester.writeToFile()
lista = fTester.readFile()
userList = []

for u in lista:
	usuario = User.User(str(u.get('username')), str(u.get('password')))
	userList.append(usuario)

for u in userList:
	print(u.username + ' ' + u.password)