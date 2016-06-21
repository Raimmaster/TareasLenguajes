"use strict";

class UserManager{
	var ulistName = 'usuarios.txt';
	var userList;

	constructor() {
		this.userList = {};

		var fs = require('fs');
		var fileStat = fs.statSync('./' + uFileName);

		if(!fileStat.isFile()){
			var wstream = fs.createWriteStream('');
			this.writeToUsersFile();
		}
	};

	createUser (username, password){
		if(this.findUser(username) !== undefined){
			this.userList[username] = password;
			return true;
		} else {
			return false;
		}
	}

	findUser (username){
		return this.userList[username];
	}

	login (username, password){
		userPass = this.findUser(username);

		if(user !== undefined){
			if(userPass === password){
				return true;
			}
		}

		return false;
	}

	writeToUsersFile (){
		var userWrite = JSON.stringify(this.userList);

		var fs = require('fs');
		fs.writeFile('./' + this.ulistName, 'utf8', function(err) {
			if(err){
				console.log(err);
			}
		});

	}

	readUsersFile (){
		var fs = require('fs');
		var fileStat = fs.statSync('./' + this.ulistName);
		if(fileStat.isFile()){
			var file = fs.readFileSync('./' + this.ulistName, 'utf8');
			this.userList = JSON.parse(file);
		}
	}

}

module.exports = UserManager;