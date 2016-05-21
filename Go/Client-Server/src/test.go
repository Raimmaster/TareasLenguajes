package main

import (
	"fmt"	
	"User"	
)

func main(){
	//u_Manager := UserManager
//	u_Manager := User.NewUserManager()
//	fmt.Println(u_Manager.QuantityUsersLoggedOn)
	if(User.ReadUsersFile()){
		fmt.Println("Hey, you!")

		for k := range User.UsersMap {
			fmt.Println(k)
		}
	}
	usu := (User.NewUser("Raim", "ara"))
	fmt.Println(User.CreateUser("Raim", "ara"))
	pas, b := User.UsersMap["Raim"]
	if b {
		fmt.Println(pas)
	}
	//usu.ChangeDir("music")
	fmt.Println(usu.Username)
	fmt.Println(usu.CurrentDir)


	for i := 1; i < 10; i++{
		fmt.Println(User.CreateUser("R" + string(i), "ara" + string(i * 2)))		
	}


	if(User.WriteToUsersFile()){
		fmt.Println("Salio...")
	}
	
}