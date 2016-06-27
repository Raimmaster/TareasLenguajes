import scala.io.StdIn._
import java.net._
import java.io._

object Client {

	val opsConDirs = Array("1", "5", "6", "7")
	val logged_options = Array("1. cd", "2. ls", "3. put (file)", "4. get", "5. rm file", "6. rmdir dir", "7. mkdir dir", "8. pwd", "9. Salir")

	def containsDirOp(option : String) : Boolean={
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
		println("Ingrese el username: ")
		var username = readLine().asInstanceOf[String]
		println("Ingrese el password: ")
		var password = readLine().asInstanceOf[String]

		enviarMensaje(username, writer)
		enviarMensaje(password, writer)
	}	

	def login(writer : ObjectOutputStream, reader : ObjectInputStream) : String={
		print("Ingrese el username: ")
		val username = readLine()
		print("Ingrese el password: ")
		val password = readLine()

		enviarMensaje(username, writer)
		enviarMensaje(password, writer)

		val respuesta = reader.readObject().asInstanceOf[String]

		return respuesta
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
    				enviarMensaje(opcion, writer)
    				response = reader.readObject().asInstanceOf[String]
    				println(response)

    				if(response == "Login:\n"){
    					mensaje = login(writer, reader)

    					if(mensaje == "Dir User:\n"){
    						println("Conexion establecida!")

    						while (mensaje != "Log Off:\n"){
    							println("Opciones: ")
    							for(valor <- 0 until logged_options.length)
    								println(logged_options(valor))

    							var selectedOption = readLine()
    							var dirName = ""
    							var fileName = ""

    							selectedOption match {
    								case "1" =>
    									println("Ingrese el nuevo directorio: ")
    									dirName = readLine() 
    							}
    							
    						}
    					}
    				}

    			case "3" => //salir
    				println("Saliendo...")
    		}
    	}

    	reader.close()
    	writer.close()
    	server.close()
	}
	
}