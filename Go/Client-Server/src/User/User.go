package User

type User struct {
	Username string
	Password string
	CurrentDir string
	PrevDir string
}

func NewUser(user, password string) *User {
	usuario := new (User)
	usuario.Username = user
	usuario.Password = password
	usuario.CurrentDir = "Usuarios/" + user
	usuario.PrevDir = usuario.CurrentDir

	return usuario
}

func (usuario *User) ChangeDir(nombreDirectorio string) bool {
	//hacer lo que tenga que hacer
	//user.User.ChangeDir("music")
	usuario.PrevDir = usuario.CurrentDir
	usuario.CurrentDir += "/" + nombreDirectorio	

	return true
}