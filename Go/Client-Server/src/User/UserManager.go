package User

import (
	"encoding/json"
	"io/ioutil"
	"fmt"
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
	if ReadUsersFile(){
		fmt.Println("Loaded users.")
	}
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
	ReadUsersFile()
	usersToWrite, error := json.Marshal(UsersMap)

	if error != nil {
		return false
	}

	f_users, err := os.Create("usuarios.txt")
	defer f_users.Close()

	if(err != nil){
		return false
	}

	//fmt.Println(usersToWrite)
	for key := range UsersMap {
		total_dirname := "Usuarios/" + key
		os.MkdirAll(total_dirname, 0777)
		//fmt.Println(key)
	}
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
	usersFile ,err := ioutil.ReadFile("usuarios.txt")	

	if err != nil {
		fmt.Print("Error opening user file.")
		return false
	}

	renewMap()
	err = json.Unmarshal(usersFile, &UsersMap)
	
	if err != nil {
		return false
	}

	for key := range UsersMap {
		total_dirname := "Usuarios/" + key
		os.MkdirAll(total_dirname, 0777)
		//fmt.Println(key)
	}

	return true	
}

func renewMap() bool {
	for key := range UsersMap {		
		delete (UsersMap, key)
	}

	return true
}