//import scala.io.StdIn.{readLine}
import java.net._
import java.io._
import java.util.concurrent._
import cliSer._

object Server {
	
	def main(args: Array[String]): Unit = {
	  val serverSocket = new ServerSocket(8888)
	  println("Server started")
	  while(true){
	  	val client:Socket = serverSocket.accept()
	  	
	  	println("Client connected: " + client.getLocalSocketAddress())

	  	new Thread( new Runnable {
	  		def run(): Unit = {
	  			handleClient(client)
	  		}
	  	}).start()
	  }

	  serverSocket.close()
	}
	
	def handleClient(client : Socket) : Unit = {
		val writer : ObjectOutputStream = new ObjectOutputStream(client.getOutputStream)
    	val reader : ObjectInputStream = new ObjectInputStream(client.getInputStream)
		
		var uManager = new UsersManager()
		uManager = uManager.readUsersFile
		
		var optionReceived = 0

		while (optionReceived != 3){

		}

		writer.close()
		reader.close()
		client.close()
		uManager.writeToUsersFile
		println("Adios")
	}

}
