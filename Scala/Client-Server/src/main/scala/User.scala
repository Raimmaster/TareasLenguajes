package cliSer

import java.io._

class User (user : String) {
	val username = user;
	var currentDir = "Usuarios/" + username;
	var prevDir = currentDir;

	var dir = new File(currentDir)

	if(!dir.exists()){
		dir.mkdir
	}

	def changeDirectory(newDir : String) : String ={//cd
		val ownDir = "Usuarios" + username
		println("New dir: " + newDir)

		if(newDir == currentDir){
			println("Ya se encuentra en ese directorio.")
		}else if (newDir == ".."){
			currentDir = prevDir
			prevDir = currentDir
		}else {
			var file = new File(currentDir)
        	val fileDirs = file.listFiles() //arreglo de archivos
        	val elDir = currentDir + "/" + newDir
        	
        	val pathNew = new File(elDir)
        	var temFile = null
        	//for para chequear si el nuevo dir existe, y si es dir
        	for(temFile <- fileDirs){
        		if(temFile.getName == newDir){
        			if( pathNew.isDirectory() ){
        				prevDir = currentDir
        				currentDir = prevDir + "/" + newDir
        			}        			
        		}
        	}
		}

		return currentDir
	}

	def listFiles : String = {
		var current = new File(currentDir)
		val filesDirs = current.listFiles()
		var f = null

		var lista = ""

		for(f <- filesDirs){
			if(f.isFile())
				lista += "*" + f.getName + "\n"
			else
				lista += "-" + f.getName + "\n"
		}

		return lista
	}

	def removeFile(filename : String) = {
		fileToRemove = currentDir + "/" + filename
		var file = new File(fileToRemove)

		if(file.exists())
			file.delete()
	}

	def removeDirectory(dirname : String) = {
		fileToRemove = currentDir + "/" + dirname
		var file = new File(fileToRemove)

		if(file.exists())
			file.delete()
	}

	def createDirectory(dirname : String) : Boolean ={
		var dirToCreate = new File(currentDir + "/" + dirname)

		if( !dirToCreate.exists() ){
			return true
		}else
			return false
	}

	def getCurrentDirName : String = {
		return currentDir
	}
}