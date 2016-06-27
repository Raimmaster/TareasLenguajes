import scala.io.StdIn._
import java.net._
import java.io._

object Client {

	val opsConDirs = Array(1, 5, 6, 7)

	def containsDirOp(option : Int) : Boolean={
		var contiene = false;

		for(valor <- opsConDirs){
			if (option == valor)
				contiene = true
		}

		return contiene
	}

	def put(fName : String, dName : String) : Unit={
		//TO-DO
	}

	def get(fName : String, dName : String) : Unit={
		//TO-DO	
	}

	def enviarMensaje(message : String, escritor : ObjectOutputStream) : Unit={
		escritor.writeObject(message)
		escritor.flush()
	}

	def createUser(writer : ObjectOutputStream) : Unit={
		var username = readLine().asInstanceOf[String]
		var password = readLine().asInstanceOf[String]

		enviarMensaje(username, writer)
		enviarMensaje(password, writer)
	}	

	def main(args: Array[String]): Unit = {
		val server = new Socket(InetAddress.getByName("localhost"), 8888)
		val reader = new ObjectInputStream(server.getInputStream)
		val writer : ObjectOutputStream = new ObjectOutputStream(server.getOutputStream)
    	
    	var response = ""
    	var mensaje = ""
    	var opcion = "0"

    	while(opcion != "3"){//main menu
    		println("1. Crear usuario. ")
    		println("2. Login. ")
    		println("3. Salir. ")

    		opcion = readLine()

    		opcion match {
    			case "1" => //crear user
    				enviarMensaje(opcion, writer)
    				response = reader.readObject().asInstanceOf[String]

    				if(response == "Ingresar usuario:\n"){
    					createUser(writer)
    					mensaje = reader.readObject().asInstanceOf[String]

    					if(mensaje == "Usuario creado\n")
    						println("Usuario creado perfectamente.")
    				}
    			case "2" => //login

    			case "3" => //salir
    				println("Saliendo...")
    		}
    	}

    	reader.close()
    	writer.close()
    	server.close()
	}
	
}