import scala.io.StdIn.{readLine}
import java.net._
import java.io._
import java.util.concurrent._
import cliSer._

object Server {
	
	val opsConDirs = Array(1, 5, 6, 7)
	
	def main(args: Array[String]): Unit = {
	  val serverSocket = new ServerSocket(8888)
	  println("Server started")
	  while(true){
	  	val client:Socket = serverSocket.accept()

	  	new Thread( new Runnable {
	  		def run(): Unit = {
	  			handleClient(client)
	  		}
	  	}).start()
	  }

	  serverSocket.close()
	}
	
	def createUser(manager : UsersManager, read : ObjectInputStream) : Boolean={
		var username = read.readObject()
		var password = read.readObject()

		var created = manager.createUser(username, password)

		println("Creado")

		return created
	}

	def enviarMensaje(message : String, escritor : ObjectOutputStream) : Unit={
		out.writeObject(message)
		out.flush()
	}

	def canLogin(username : String, manager : UsersManager, read : ObjectInputStream) : Boolean={
		var password = read.readObject()
		val canLog = manager.login(username, password)

		return canLog
	}

	def containsDirOp(option : Int) : Boolean={
		var contiene = false;

		for(valor <- opsConDirs){
			if (option == valor)
				contiene = true
		}

		return contiene
	}

	def put(user : User, fName : String) : Unit={
		//TO-DO
	}

	def get(user : User, fName : String) : Unit={
		//TO-DO	
	}

	def handleClient(client : Socket) : Unit = {
		val writer : ObjectOutputStream = new ObjectOutputStream(client.getOutputStream)
    	val reader : ObjectInputStream = new ObjectInputStream(client.getInputStream)
		
		var uManager = new UsersManager()		
		uManager = uManager.readUsersFile
		
		var optionReceived = 0
		//loop del main menu
		while (optionReceived != 3){
			println("Se obtuvo conexión de cliente.")
			optionReceived = reader.readObject()
			var mensajeEnviar = ""
			//el equivalente a switch
			optionReceived match {
				case 1 => //create user
					mensajeEnviar = "Ingresar usuario:\n"
					enviarMensaje(mensajeEnviar)
					createUser(client, reader)
					mensajeEnviar = "Usuario creado\n"
					enviarMensaje(mensajeEnviar)
				case 2 => //login
					mensajeEnviar = "Login:\n"
					var username = reader.readObject()
					enviarMensaje(mensajeEnviar)

					if(canLogin(username, uManager, reader)){//if can login, new loop
						mensajeEnviar = "Dir User:\n"
						println("Loggineado")
						var loggedUser = new User(username)
						enviarMensaje(mensajeEnviar)
						//variables para file work
						var dirName = ""
						var fileName = ""

						while (optionReceived != 9){//logged user loop
							optionReceived = reader.readObject()

							if(containsDirOp(optionReceived))
								dirName = reader.readObject()
							
							if(optionReceived == 3 || optionReceived == 4){
								println("Opcion: " + optionReceived)
								fileName = reader.readObject()
							}

							optionReceived match {//user's menu options
								case 1 => //cd
									loggedUser.changeDirectory(dirName)
									mensajeEnviar = "cd\n"
								case 2 => //ls
									var filesList = loggedUser.listFiles()
									mensajeEnviar = "ls\n"
									writer.writeObject(filesList)
									//time.sleep(0.3)									
								case 3 => //put
									put(loggedUser, fileName)
									mensajeEnviar = "Written\n"
									println("Archivo obtenido")
								case 4 => //get
									get(loggedUser, fileName)
									mensajeEnviar = "Sent\n"
								case 5 => //rm file
									loggedUser.removeFile(dirName)
									mensajeEnviar = "rm\n"
								case 6 => //rmdir
									loggedUser.removeDirectory(dirName)
									mensajeEnviar = "rmdir\n"
								case 7 => //mkdir
									loggedUser.createDirectory(dirName)
									mensajeEnviar = "mkdir\n"
								case 8 => //pwd									
									var estoy = loggedUser.getCurrentDirName()
									mensajeEnviar = "pwd\n"
									writer.writeObject(estoy)
									//time.sleep(0.3)
								case 9 => //exit
									println("Logging user off...")
									mensajeEnviar = "Log Off:\n"
							}

							if(optionReceived != 4)
								writer.writeObject(mensajeEnviar)
						}
					}
				case 3 => //exit
					println("Exiting...")
			}
		}

		writer.close()
		reader.close()
		client.close()
		uManager.writeToUsersFile
		println("Adios")
	}
}
