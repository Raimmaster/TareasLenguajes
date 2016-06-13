var ulistName = 'usuarios.txt';
var userList;

function UserManager() {
	this.userList = {};

	var fs = require('fs');
	var fileStat = fs.statSync('./' + uFileName);

	if(!fileStat.isFile()){
		var wstream = fs.createWriteStream('');
		this.writeToUsersFile();
	}


};

UserManager.prototype.createUser = function (username, password){
	if(this.findUser(username) !== undefined){
		this.userList[username] = password;
		return true;
	} else {
		return false;
	}
}

UserManager.prototype.findUser = function (username){
	return this.userList[username];
}

UserManager.prototype.login = function(username, password){
	userPass = this.findUser(username);

	if(user !== undefined){
		if(userPass === password){
			return true;
		}
	}

	return false;
}

UserManager.prototype.writeToUsersFile = function (){
	var userWrite = JSON.stringify(this.userList);

	var fs = require('fs');
	fs.writeFile('./' + this.ulistName, 'utf8', function(err) {
		if(err){
			console.log(err);
		}
	});

}

UserManager.prototype.readUsersFile = function (){
	var fs = require('fs');
	var fileStat = fs.statSync('./' + this.ulistName);
	if(fileStat.isFile()){
		var file = fs.readFileSync('./' + this.ulistName, 'utf8');
		this.userList = JSON.parse(file);
	}
}