package main

import (
	"fmt"
	"net"
    "bufio"
    "os"
)

func client() {
    // connect to the server
    c, err := net.Dial("tcp", ":9999")
    
    if err != nil {
        fmt.Println(err)
        return
    }

    // send the message
    msg := "Hello World"
    fmt.Println("Sending", msg)
    //err = gob.NewEncoder(c).Encode(msg)
    reader := bufio.NewReader(os.Stdin)
    fmt.Print("Texto: ")
    text, _ := reader.ReadString('\n')

    //cant, err := c.Write([]byte(msg))
    
    //send
    fmt.Fprintf(c, text + "\n")
    //get messsage
    message, err := bufio.NewReader(c).ReadString('\n')

    if err != nil {
        fmt.Println(err)
    }

    fmt.Println(message)

    c.Close()
}

func main() {
    //go server()
    /*go*/
    client()

    var input string
    fmt.Scanln(&input)
}