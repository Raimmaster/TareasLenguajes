package main

import (
	//"encoding/json"
	//"io/ioutil"
	//"encoding/gob"
	"os"
	"fmt"
	"net"
 	"time"
 	"bufio"
 	"strings"
	"strconv"
)


var opsConDirs = []int{1, 5, 6, 7}

var logged_options = []string{"1. cd", "2. ls", "3. put (file)", 
	"4. get", "5. rm file", "6. rmdir dir", 
	"7. mkdir dir", "8. pwd", "9. Salir"}

const DIRS_SIZE = 4
const reading_size = 1024

func getUserMessage(cli_sock net.Conn, reader *bufio.Reader) string {
		fmt.Print("\nIngrese el username: ")    	
		username,_:= reader.ReadString('\n')
		fmt.Print("\nIngrese el password: ")    	
	    password,_:= reader.ReadString('\n')
	    //Enviar al servidor
	    cli_sock.Write([]byte(username))
	    cli_sock.Write([]byte(password))				
		mensaje, _ := bufio.NewReader(cli_sock).ReadString('\n')

		return mensaje
}

func Min(x, y int) int {
    if x < y {
        return x
    }

    return y
}

func main(){
    client_socket, err := net.Dial("tcp", ":8888")

    if err != nil {
    	fmt.Println(err)
    	return
    }

    opcion := 0
    //para entradas de texto
    reader := bufio.NewReader(os.Stdin)
    for ; opcion != 3; {
    	fmt.Println("\n1. Crear usuario.")    	
    	fmt.Println("2. Login.")
    	fmt.Println("3. Salir.")
    	fmt.Print("\nEscribir opcion: ")    	
    	opInput,_:= reader.ReadString('\n')
		opcion, _ = strconv.Atoi(strings.TrimSpace(string(opInput)))
		var file_name string
		var file_path string
		fmt.Println(opcion)
		switch opcion {
			case 1://create user
				//para enviar del socket al server
				client_socket.Write([]byte(opInput))

				response, err := bufio.NewReader(client_socket).ReadString('\n')

				if err != nil {
					fmt.Println(err)
				}
				fmt.Println(response)
				if strings.TrimSpace(response) == "Ingresar usuario:"{
					mensaje := getUserMessage(client_socket, reader)
					if strings.TrimSpace(mensaje) == "Usuario creado" {
						fmt.Println("Usuario creado exitosamente.")
					} else {
						fmt.Println("El usuario no fue creado. Quiza ya existia.")
					}
				}
			case 2: //login
				client_socket.Write([]byte(opInput))
				response, _ := bufio.NewReader(client_socket).ReadString('\n')
				fmt.Println(response)

					if strings.TrimSpace(response) == "Login" {				
						mensaje := getUserMessage(client_socket, reader)

						if strings.TrimSpace(mensaje) == "Dir User:" {//conectado
							fmt.Println("Conexion establecida!")

							var data_con string = ""
							//data_con := " "
							for ; strings.TrimSpace(data_con) != "Log Off:"; {
								fmt.Println("Opciones:\n")
								for _, valor := range logged_options {
								    fmt.Printf("%v \n", valor)
								}

								fmt.Print("Elegir: ")
								selectedOption := 0
								opInput, _ := reader.ReadString('\n')
								selectedOption,_ = strconv.Atoi(strings.TrimSpace(opInput))
								var dir_name string
								switch selectedOption {
									case 1: //cd
										fmt.Println("Ingrese el nuevo dir a estar: ")
										dir_name, _ = reader.ReadString('\n')
									case 2: //ls
										fmt.Println("Listar dirs: \n")
									case 3: //put
										fmt.Println("Ingrese el path del archivo a subir: ")
										dir_name, _ = reader.ReadString('\n')
										fmt.Println("Ingrese el nombre del nuevo archivo: ")
										file_name, _ = reader.ReadString('\n')
									case 4: //get
										fmt.Println("Ingrese el nombre del nuevo archivo: ")
										file_name, _ = reader.ReadString('\n')
										fmt.Println("Ingrese el path donde estara: ")
										file_path, _ = reader.ReadString('\n')
									case 5: //rm file
										fmt.Println("Ingrese el nombre del archivo a eliminar: ")
										dir_name, _ = reader.ReadString('\n')
									case 6: //rmdir
										fmt.Println("Ingrese el nombre del directorio a eliminar: ")
										dir_name, _ = reader.ReadString('\n')
									case 7: //mkdir
										fmt.Println("Ingrese el nombre del directorio a crear: ")
										dir_name, _ = reader.ReadString('\n')
									case 8: //pwd
										fmt.Println("Me encuentro en: ")
									case 9: //exit
										fmt.Println("Logging out.")
								}

								client_socket.Write([]byte(opInput))
								//chequear si se debe enviar un dir name
								for i := 0; i < DIRS_SIZE; i++ {
									if selectedOption == opsConDirs[i] {
										client_socket.Write([]byte(dir_name))
										break
									}
								}

								switch selectedOption {
									case 2:
										files_list, _ := bufio.NewReader(client_socket).ReadString('\n')										
										fmt.Println(files_list)
									case 3://sending files
										time.Sleep(300 * time.Millisecond)
										file, _ := os.Open(dir_name)
				  						defer file.Close()
				  						//file info
				  						file_info, _ := file.Stat()
				  						file_size := file_info.Size()
				  						//send file's size
				  						client_socket.Write([]byte(file_name))
				  						time.Sleep(200 * time.Millisecond)
				  						client_socket.Write([]byte(string(file_size)))
				  						time.Sleep(200 * time.Millisecond)
				  						//send file
				  						size_read := 0
			  							quant := Min(int(file_size) - size_read, reading_size)

			  							for file_size > 0 {
			  								data := make([]byte, Min(int(int(file_size) - quant), size_read))	
			  								quant, _ := file.Read(data)  								
			  								client_socket.Write(data)

			  								file_size -= int64(quant)
			  							}
			  							fmt.Println("Archivo enviado.")				  						
									case 4://reading file
										client_socket.Write([]byte(file_name))
										//get the size to be reading
										val, _ := bufio.NewReader(client_socket).ReadString('\n')
										file_size, _ := strconv.Atoi(val)
										size_read := 0
										var cant_read int
										//Writing file
			  							n_file, _ := os.Create(file_path)
			  							defer n_file.Close()
			  							
			  							if file_size < reading_size {
			  								cant_read = file_size	  								
			  							} else {									
			  								cant_read = reading_size
										}
										clReader := bufio.NewReader(client_socket)	  	
										//func (f *File) ReadAt(b []byte, off int64) (n int, err error)
										var data [] byte
										cant_read, _ = clReader.Read(data)

										for cant_read > 0 {
											n_file.Write(data)
											cant_read = Min(int(file_size) - size_read, reading_size)
											if cant_read == 0 {
												break
											}

											cant_read, _ = clReader.Read(data)
										}
									case 8://receive pwd
										pwd_mess, _ := bufio.NewReader(client_socket).ReadString('\n')
										fmt.Println(pwd_mess)
									default: 
										fmt.Print("")										
								}

								//final data
								if selectedOption != 4 {
									data_con, _ = bufio.NewReader(client_socket).ReadString('\n')
								} else {
									data_con = "Sent"
								}

								fmt.Println("Data con: ", data_con)								
							} 
						}
					}

			case 3:
				client_socket.Close()
				fmt.Println("Saliendo...")
		}
    }
}