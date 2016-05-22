package main

import (
	//"encoding/json"
	"fmt"
	//"io/ioutil"
	//"os"
	//"encoding/gob"
	"net"
 	"log"
 	"bufio"
 	"User"
 	"time"
)


var opsConDirs = []int{1, 5, 6, 7}
const DIRS_SIZE = 4
func main() {
	//server connection

	server_socket, err := net.Listen("tcp", ":9999")
	
	uManager := User.NewUserManager()
	print(uManager.QuantityUsersLoggedOn)
	
	if err != nil {
		log.Fatal(err)
		return
	}

	for {
		client_socket, err := server_socket.Accept()

		if err != nil {
			fmt.Println(err)
			continue
		}

		go handleClientThreadConnection(client_socket)
	}

}

func getUserInfo(reader *bufio.Reader) (username, password string){
	user, err := reader.ReadString('\n')
	  			
	if (err != nil) {
		fmt.Println(err)
		return " ", " "
	}

	pass, err := reader.ReadString('\n')
		
	if (err != nil) {
		fmt.Println(err)
		return " ", " "
	}	

	return string(user), string(pass)
}

func checkOptions(option int) bool {
	for i := 0; i < DIRS_SIZE; i++ {
		if(option == opsConDirs[i])
			return true
	}

	return false
}

func handleClientThreadConnection(cli_sock net.Conn){
	
	optionReceived := 0

	fmt.Println("Opciones con directorios: ", opsConDirs)

	for ; optionReceived != 3; {
		fmt.Println("Conexion con: ", cli_sock.RemoteAddr())
		
		//err := gob.NewDecoder(c).Decode(&message)
	  	reader := bufio.NewReader(cli_sock)	  	
	  	valor_menu, _, err := reader.ReadRune()
	  	optionReceived = int(valor_menu)
	  	//fmt.Println(cant)
	  	
	  	if err != nil {
	  		fmt.Println("Error ", err)
	  		continue
	  	}

	  	fmt.Println("Mensaje: ", string(optionReceived))
	  	
	  	var mensaje_enviar string

	  	switch optionReceived {
	  		case 1://create user
	  			mensaje_enviar = "Ingresar usuario:"
	  			cli_sock.Write([]byte(mensaje_enviar))
	  			/*user, err := reader.ReadString('\n')
	  			
	  			if (err != nil) {
	  				fmt.Println(err)
	  			}

	  			pass, err := reader.ReadString('\n')
	  			*/

	  			user, pass := getUserInfo(reader)

	  			if User.CreateUser(string(user), string(pass)) {
	  				mensaje_enviar = "Usuario creado"
	  			}else {
	  				mensaje_enviar = "Ya existe"
	  			}

	  			User.WriteToUsersFile()
	  			cli_sock.Write([]byte(mensaje_enviar))
	  			fmt.Println("Creado")
	  		case 2://login
	  			mensaje_enviar = "Login"
	  			cli_sock.Write([]byte(mensaje_enviar))

	  			user, pass := getUserInfo(reader)
	  			if User.Login(user, pass) {
	  				mensaje_enviar = "Dir User:"
	  				fmt.Println("Loggineado")
	  				loggedUser = User.NewUser(user, pass)
	  				cli_sock.Write([]byte(mensaje_enviar))
	  				dir_name := ""
	  				file_name := ""
	  				files_list := ""
	  				for {
	  					valor_menu, _, err := reader.ReadRune()
	  					optionReceived = int(valor_menu)

	  					if checkOptions(option) {
	  						dir_name = reader.ReadString('\n')
	  					}

	  					if err != nil {
	  						fmt.Println(err)
	  						optionReceived = 2
	  						continue
	  					}	  					

	  					switch optionReceived {
	  						case 1: //cd
	  							loggedUser.ChangeDir(dir_name)
	  							mensaje_enviar = "cd"
	  						case 2: //ls
	  							files_list = loggedUser.ListFiles()
	  							mensaje_enviar = "ls"
	  							cli_sock.Write([]byte(mensaje_enviar))
	  							time.Sleep(100 * time.Millisecond)
	  						case 3: //put
	  							
	  						case 4: //get
	  						case 5: //rm file
	  						case 6: //rmdir
	  						case 7: //mkdir
	  						case 8: //pwd
	  						case 9: //exit
	  					}
	  				}
	  			}
	  		case 3:

	  	}

	  	//opcion,err:= strconv.Atoi(strings.TrimSpace(string(message)))
	  	cli_sock.Write([]byte("Has been received.\n"))
		//optionReceived := int()
		optionReceived = 3
	}

	cli_sock.Close()	
}
