package User

var usersMap = make(map[string]string)

func UserExists(username string) (password string){
	password, ok := usersMap[username]

	if(!ok){
		return ""
	}

	return 
}

func CreateUser(username, password string) bool {
	if UserExists(username) == ""{
		usersMap[username] = password

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
