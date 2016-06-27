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
		var username = read.readObject().asInstanceOf[String]
		var password = read.readObject().asInstanceOf[String]

		var created = manager.createUser(username, password)

		println("Creado")

		return created
	}

	def enviarMensaje(message : String, escritor : ObjectOutputStream) : Unit={
		escritor.writeObject(message)
		escritor.flush()
	}

	def canLogin(username : String, manager : UsersManager, read : ObjectInputStream) : Boolean={
		var password = read.readObject().asInstanceOf[String]
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
			optionReceived = reader.readObject().asInstanceOf[Int]
			var mensajeEnviar = ""
			//el equivalente a switch
			optionReceived match {
				case 1 => //create user
					mensajeEnviar = "Ingresar usuario:\n"
					enviarMensaje(mensajeEnviar, writer)
					createUser(uManager, reader)
					mensajeEnviar = "Usuario creado\n"
					enviarMensaje(mensajeEnviar, writer)
				case 2 => //login
					mensajeEnviar = "Login:\n"
					var username = reader.readObject().asInstanceOf[String]
					enviarMensaje(mensajeEnviar, writer)

					if(canLogin(username, uManager, reader)){//if can login, new loop
						mensajeEnviar = "Dir User:\n"
						println("Loggineado")
						var loggedUser = new User(username)
						enviarMensaje(mensajeEnviar, writer)
						//variables para file work
						var dirName = ""
						var fileName = ""

						while (optionReceived != 9){//logged user loop
							optionReceived = reader.readObject().asInstanceOf[Int]

							if(containsDirOp(optionReceived))
								dirName = reader.readObject().asInstanceOf[String]
							
							if(optionReceived == 3 || optionReceived == 4){
								println("Opcion: " + optionReceived)
								fileName = reader.readObject().asInstanceOf[String]
							}

							optionReceived match {//user's menu options
								case 1 => //cd
									loggedUser.changeDirectory(dirName)
									mensajeEnviar = "cd\n"
								case 2 => //ls
									var filesList = loggedUser.listFiles()
									mensajeEnviar = "ls\n"
									enviarMensaje(filesList, writer)
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
									enviarMensaje(estoy, writer)
									//time.sleep(0.3)
								case 9 => //exit
									println("Logging user off...")
									mensajeEnviar = "Log Off:\n"
							}

							if(optionReceived != 4)
								enviarMensaje(mensajeEnviar, writer)
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
