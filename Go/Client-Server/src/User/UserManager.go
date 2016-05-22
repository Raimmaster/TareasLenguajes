package User

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
//	"log"
)

type UserManager struct{
	QuantityUsersLoggedOn int
}

var UsersMap = make(map[string]string)

func NewUserManager() *UserManager {
	u_Manager := new (UserManager)
	u_Manager.QuantityUsersLoggedOn = 0
	return u_Manager
}

func UserExists(username string) (password string){
	password, ok := UsersMap[username]

	if(!ok){
		return ""
	}

	return 
}

func CreateUser(username, password string) bool {
	if UserExists(username) == ""{
		UsersMap[username] = password

		return true		
	}

	return false	
}

func Login(username, password string) bool{
	pass := UserExists(username)
	if pass == password {
		return true
	}

	return false	
}

func WriteToUsersFile() bool{
	usersToWrite, error := json.Marshal(UsersMap)

	if error != nil {
		return false
	}

	f_users, err := os.Create("usuarios.txt")
	defer f_users.Close()

	if(err != nil){
		return false
	}

	fmt.Println(usersToWrite)
	
	//errors := ioutil.WriteFile("Usuarios.txt", usersToWrite, 0777)
	
	_, errors := f_users.Write(usersToWrite)	
	
	if errors != nil {
		fmt.Println("Not written...")		
		return false
	}

	fmt.Println("Written...")
	
	return true
}

func ReadUsersFile() bool{
	//var users []User
	usersFile ,err := ioutil.ReadFile("Usuarios.txt")
	
	if err != nil {
		fmt.Print("Error opening user file.")
		return false
	}

	renewMap()
	err = json.Unmarshal(usersFile, &UsersMap)
	
	if err != nil {
		return false
	}

	return true	
}

func renewMap() bool {
	for key := range UsersMap {
		delete (UsersMap, key)
	}

	return true
}