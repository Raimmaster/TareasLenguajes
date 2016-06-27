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

	//get files from server
	def get(filePath : String,
		fileName : String,
		reader : ObjectInputStream,
		writer : ObjectOutputStream) : Unit={

		enviarMensaje(fileName, writer)
		var fileSize = reader.readObject.asInstanceOf[String].toInt
		
		var pathWrite = filePath + "/" + fileName

		var nFile = new FileOutputStream(pathWrite)
		var cantRead = fileSize

		while (cantRead > 0){//mientras no se haya leído todo
			val data = new Array[Byte](Math.min(fileSize, 1024))
			reader.read(data) //read from socket
			nFile.write(data) //write to file
			cantRead -= data.length
		}
	}

	//send files to server
	def put(fName : String,
		dirName : String,
		writer : ObjectOutputStream) : Unit={

		val sFile = new FileInputStream(dirName)
		val f = new File(dirName)
		enviarMensaje(fName, writer)

		var fileSize = f.length()
		var fSizeSend = fileSize.toString
		enviarMensaje(fSizeSend, writer)
		
		while (fileSize > 0){ //mientras no hayamos terminado de leer
			val data = new Array[Byte](Math.min(fileSize.toInt, 1024))
			sFile.read(data)
			writer.write(data)
			writer.flush()

			fileSize -= data.length
		}

		println("Archivo enviado.")
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

    						while (mensaje != "Log Off:\n"){ //logged user loop
    							println("Opciones: ")
    							for(valor <- 0 until logged_options.length)
    								println(logged_options(valor))

    							var selectedOption = readLine()
    							var dirName = ""
    							var fileName = ""
    							var filePath = ""
    							selectedOption match {
    								case "1" => //cd
    									println("Ingrese el nuevo directorio: ")
    									dirName = readLine()
    								case "2" => //ls
    									println("Listar directorios: ")
    								case "3" => //put
    									println("Ingrese el path del archivo a subir: ")
    									dirName = readLine()
    									println("Nombre de nuevo archivo: ")
    									fileName = readLine()
    								case "4" => //get
    									println("Ingrese el nombre nuevo archivo: ")
    									fileName = readLine()
    									println("Ingrese el path donde estara: ")
    									filePath = readLine()
    								case "5" => //rm file
    									println("Ingrese el nombre del archivo a eliminar: ")
    									dirName = readLine()
    								case "6" => //rmdir
    									println("Ingrese el nombre del directorio a eliminar: ")
    									dirName = readLine()
    								case "7" => //mkdir
    									println("Ingrese el path del directorio a crear: ")
    									dirName = readLine()
    								case "8" => //pwd
    									print("Me encuentro en: ")
    								case "9" => //exit
    									println("Log off...")
    							}
    							
    							enviarMensaje(selectedOption, writer)

    							if(containsDirOp(selectedOption))
    								enviarMensaje(dirName, writer)

    							selectedOption match {
    								case "2" =>
	    								val filesList = reader.readObject().asInstanceOf[String]
	    								println(filesList)
	    							case "3" =>
    									put(fileName, dirName, writer)
	    							case "4" =>
    									get(filePath, fileName, reader, writer)
	    							case "8" =>
	    								val estoy = reader.readObject().asInstanceOf[String]
	    								println(estoy)
    							}

    							if(selectedOption != "4")
    								mensaje = reader.readObject().asInstanceOf[String]
    							else
    								mensaje = "Sent"

    							println(mensaje)
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