package main

import (
	//"encoding/json"
	//"io/ioutil"
	//"encoding/gob"
	"os"
	"fmt"
	"net"
 	"bufio"
 	"User"
 	"time"
)


var opsConDirs = []int{1, 5, 6, 7}

logged_options := {"1. cd", "2. ls", "3. put (file)", 
	"4. get", "5. rm file", "6. rmdir dir", 
	"7. mkdir dir", "8. pwd", "9. Salir"}

const DIRS_SIZE = 4

func main(){
    client_socket, err := net.Dial("tcp", ":8888")

    if err != nil {
    	fmt.Println(err)
    	return
    }

    opcion := 0
    //para entradas de texto
    reader := bufio.NewReader(os.Stdin)
    //optxt,_:= reader.ReadString('\n')

/*    message, _ = bufio.NewReader(conn).ReadString('\n')
				if message!="Success\n" {
					fmt.Print(message)
					text, _ := reader.ReadString('\n')
					conn.Write([]byte(text))*/
    for ; opcion != 3; {

    }
}