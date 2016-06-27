package cliSer

import scala.collection.mutable.{Map => MMap}

class UsersManager extends Serializable {
	var usersList = MMap[String, String]()

	def userExists(username: String): String={
		if(usersList.contains(username)){
			return usersList(username)
		}else {
			return ""
		}
	}

	def createUser(username: String, password: String): Boolean={
		val password = userExists(username)

		if(password != ""){
			usersList += (username -> password)
			return true
		} else {
			return false
		}
	}

	def login(username: String, password: String): Boolean={
		val pass = userExists(username)
		var canLogIn : Boolean = false
		
		if(pass != ""){
			if(password == pass){
				canLogIn = true
			}
		}

		return canLogIn
	}

	def writeToUsersFile {
		import java.io._

		val writer = new ObjectOutputStream(new FileOutputStream("usuarios.txt"))
		writer.writeObject(this)
		writer.close()
	}

	def readUsersFile : UsersManager={
		import java.io._
		var uManager : UsersManager = null

		val file = new File("usuarios.txt")
		if (file.exists()){
			val reader = new ObjectInputStream(new FileInputStream("usuarios.txt"))
			uManager = reader.readObject().asInstanceOf[UsersManager]
		}else {
			uManager = new UsersManager()
		}

		return uManager
	}
}