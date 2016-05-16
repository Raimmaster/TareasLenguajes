package main

import "fmt"
import "User"	

func main(){
	usu := (User.NewUser("Raim", "ara"))
	usu.ChangeDir("music")
	fmt.Println(usu.Username)
	fmt.Println(usu.CurrentDir)
}