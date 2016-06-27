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

					}
				case 3 => //exit

			}
		}

		writer.close()
		reader.close()
		client.close()
		uManager.writeToUsersFile
		println("Adios")
	}

	def containsDirOp(option : Int) : Boolean={
		var contiene = false;

		for(valor <- opsConDirs){
			if (option == valor)
				contiene = true
		}

		return contiene
	}
}
