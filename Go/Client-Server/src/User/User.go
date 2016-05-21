package User

import (
	"fmt"
	"os"
	"io/ioutil"
	"log"
)

type User struct {
	Username string
	Password string
	CurrentDir string
	PrevDir string
}

func NewUser(user, password string) *User {
	usuario := new (User)
	usuario.Username = user
	usuario.Password = password
	usuario.CurrentDir = "Usuarios/" + user
	usuario.PrevDir = usuario.CurrentDir

	return usuario
}

func (user *User) RemoveFile(filename string) bool{
	file_to_remove := user.CurrentDir + "/" + filename
	file_stat, error := os.Stat(file_to_remove)			

	if error != nil{
		return false
	}

	if file_stat.IsDir(){
		return false //es directorio; borrar
	}

	err := os.Remove(file_to_remove)

	if err != nil{
		return false
	}

	return true
}

func (user *User) RemoveDir(filename string) bool{
	dir_to_remove := user.CurrentDir + "/" + filename
	err := os.RemoveAll(dir_to_remove)

	if err != nil{
		return false
	}

	return true	
}

func CreateDir(user *User, dirname string) bool{
	total_dirname := user.CurrentDir + "/" + dirname

	err := os.MkdirAll(total_dirname, 0777)

	if(err != nil){		
		return false
	}

	return true
}

func ListFiles(user *User) string{//ls
	var files_names string
	files_names = "\n"

	files, err := ioutil.ReadDir(user.CurrentDir)
	
	if err != nil{
		return " "
	}

	for _, file := range files {
		files_names += file.Name() + "\n"
	}

	return files_names		
} 

func GetCurrentDirName(user *User) string{
	return user.CurrentDir
}

func (usuario *User) ChangeDir(nombreDirectorio string) bool {//cd
	//hacer lo que tenga que hacer
	//user.User.ChangeDir("music")
	//own_dir := "Usuarios/" + usuario.Username

	if(nombreDirectorio == "..") {//if I have to return
		usuario.CurrentDir = usuario.PrevDir
		usuario.PrevDir = usuario.CurrentDir
		return true
	} else { 
		files, err := ioutil.ReadDir(usuario.CurrentDir)

		if err != nil {
			log.Fatal(err)

			return false
		}

		dirToCheck := usuario.CurrentDir + "/"
 		//list all files, iterate through them
		for _, file := range files {
			file_stat, err := os.Stat(dirToCheck + file.Name())
			
			if err != nil{
				return false
			}
			//check if it's not a directory to enter there
			if(file.Name() == nombreDirectorio && !file_stat.IsDir()){
				usuario.PrevDir = usuario.CurrentDir
				usuario.CurrentDir = usuario.PrevDir + "/" + nombreDirectorio
				fmt.Println(usuario.CurrentDir)
				return true
			}			
		}

		return false
	}
	
	return false
}