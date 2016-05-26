package main

import (
	//"encoding/json"
	//"io/ioutil"
	//"encoding/gob"
	"os"
	"io"
	"fmt"
	"net"
 	"log"
 	"User"
 	"time"
 	"bufio"
	"strconv"	
	"strings"
)


var opsConDirs = []int{1, 5, 6, 7}
const DIRS_SIZE = 4
func main() {
	//server connection

	server_socket, err := net.Listen("tcp", ":8888")
	
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

	return strings.TrimSpace(user), strings.TrimSpace(pass)
}

func checkOptions(option int) bool {
	for i := 0; i < DIRS_SIZE; i++ {
		if(option == opsConDirs[i]){
			return true
		}
	}

	return false
}

func Min(x, y int) int {
    if x < y {
        return x
    }

    return y
}

//function for each thread connection
func handleClientThreadConnection(cli_sock net.Conn){
	
	var optionReceived int = 0 

	for ; optionReceived != 3; {
		fmt.Println("Conexion con: ", cli_sock.RemoteAddr())
		
		//err := gob.NewDecoder(c).Decode(&message)
	  	reader := bufio.NewReader(cli_sock)	  	
	  	valor_menu, err := reader.ReadString('\n')
	  	optionReceived, _ = strconv.Atoi(strings.TrimSpace(string(valor_menu)))
	  	//fmt.Println(cant)
	  	
	  	if err != nil && err == io.EOF {
	  		fmt.Println("Logged user off")
	  		return
	  	}

	  	fmt.Println("Opcion: ", string(optionReceived))
	  	
	  	var mensaje_enviar string

	  	switch int(optionReceived) {
	  		case 1://create user
	  			mensaje_enviar = "Ingresar usuario:\n"
	  			cli_sock.Write([]byte(mensaje_enviar))
	  			user, pass := getUserInfo(reader)

	  			if User.CreateUser(string(user), string(pass)) {
	  				mensaje_enviar = "Usuario creado\n"
	  			}else {
	  				mensaje_enviar = "Ya existe\n"
	  			}

	  			User.WriteToUsersFile()
	  			cli_sock.Write([]byte(mensaje_enviar))
	  			fmt.Println("Creado")
	  		case 2://login
	  			mensaje_enviar = "Login\n"
	  			fmt.Println("Going to log")
	  			cli_sock.Write([]byte(mensaje_enviar))

	  			user, pass := getUserInfo(reader)
	  			if User.Login(user, pass) {
	  				mensaje_enviar = "Dir User:\n"
	  				fmt.Println("Loggineado")
	  				loggedUser := User.NewUser(user, pass)
	  				cli_sock.Write([]byte(mensaje_enviar))
	  				dir_name := ""
	  				file_name := ""
	  				files_list := ""
	  				for {
	  					valor_menu, err := reader.ReadString('\n')
	  					fmt.Printf("valor menu: %s \n",valor_menu)
	  					optionReceived, _ = strconv.Atoi(strings.TrimSpace(valor_menu))
	  					fmt.Println("Log option:", string(optionReceived))
	  					if err != nil {
	  						if err == io.EOF {
	  							fmt.Println("User cut connection.")
	  							return
	  						}

	  						fmt.Println(err)
	  						optionReceived = 2
	  						continue
	  					}	  					

	  					if checkOptions(optionReceived) {
	  						fmt.Println("Opciones, checking")
	  						dir_name, err = reader.ReadString('\n')
	  						if err != nil {
	  							fmt.Println(err)
	  							continue
	  						}
	  					}

	  					if optionReceived == 3 || optionReceived == 4 {
	  						fmt.Println("Opcion 3 o 4")
	  						file_name, err = reader.ReadString('\n')

	  						if err != nil {
	  							fmt.Println(err)
	  							continue
	  						}
	  					}

						//buffer size when reading or writing
						reading_size := 1024
						var cant_read int
	  					fmt.Printf("Still: %d", optionReceived)
	  					switch (optionReceived) {
	  						case 1: //cd
	  							loggedUser.ChangeDir(dir_name)
	  							mensaje_enviar = "cd\n"
	  						case 2: //ls
	  							files_list = loggedUser.ListFiles()
	  							mensaje_enviar = "ls\n"
	  							cli_sock.Write([]byte(files_list))
	  							time.Sleep(100 * time.Millisecond)
	  						case 3: //put
	  							dir_to_write := loggedUser.GetCurrentDirName()
	  							val, err := reader.ReadString('\n')
	  							
	  							if err != nil {
	  								fmt.Println(err)
	  								continue
	  							}

	  							file_size, _ := strconv.Atoi(val)
	  							size_read := 0

	  							path_write := dir_to_write + "/" + file_name

	  							n_file, _ := os.Create(path_write)
	  							defer n_file.Close()
	  							
	  							if file_size < reading_size {
	  								cant_read = file_size	  								
	  							} else {									
	  								cant_read = reading_size
								}

								//func (f *File) ReadAt(b []byte, off int64) (n int, err error)
								var data [] byte
								cant_read, _ = reader.Read(data)

								for cant_read > 0 {
									n_file.Write(data)
									cant_read = Min(file_size - size_read, reading_size)
									if cant_read == 0 {
										break
									}

									cant_read, _ = reader.Read(data)
								}

								mensaje_enviar = "Written\n"
								fmt.Println("Obtuve archivo")
	  						case 4: //get
	  							file_dir := loggedUser.GetCurrentDirName()
	  							file_path := file_dir + "/" + file_name
	  							file, _ := os.Open(file_path)
	  							defer file.Close()
	  							file_info, _ := file.Stat()
	  							file_size := file_info.Size()	  							
	  							time.Sleep(100 * time.Millisecond)
	  							cli_sock.Write([]byte(strconv.Itoa(int(file_size))))	  							
	  							time.Sleep(300 * time.Millisecond)
	  							size_read := 0
	  							quant := Min(int(file_size) - size_read, reading_size)

	  							for file_size > 0 {
	  								data := make([]byte, Min(int(int(file_size) - quant), size_read))	
	  								quant, _ := file.Read(data)  								
	  								cli_sock.Write(data)

	  								file_size -= int64(quant)
	  							}

	  							fmt.Println("Enviado")
	  							mensaje_enviar = "Sent\n"
	  						case 5: //rm file
	  							loggedUser.RemoveFile(file_name)
	  							mensaje_enviar = "rm\n"
	  						case 6: //rmdir
	  							loggedUser.RemoveDir(dir_name)
	  							mensaje_enviar = "rmdir\n"
	  						case 7: //mkdir
	  							loggedUser.CreateDir(dir_name)
	  							mensaje_enviar = "mkdir\n"
	  						case 8: //pwd
	  							estoy := loggedUser.GetCurrentDirName()
	  							mensaje_enviar = "pwd\n"
	  							cli_sock.Write([]byte(estoy))
	  							time.Sleep(300 * time.Millisecond)
	  						case 9: //exit
	  							fmt.Println("Logging off user: ", loggedUser.Username)
	  							mensaje_enviar = "Log Off:\n"
	  					}

	  					if (optionReceived != 4) {
	  						cli_sock.Write([]byte(mensaje_enviar))
	  					}

	  					if optionReceived == 9 {
	  						break
	  					}
	  				}
	  			}
	  	}

	  	//opcion,err:= strconv.Atoi(strings.TrimSpace(string(message)))
	  	cli_sock.Write([]byte("Has been received.\n"))
		//optionReceived := int()
		//optionReceived = 3
	}

	User.WriteToUsersFile()
	cli_sock.Close()	
	fmt.Println("Adios")	
}
