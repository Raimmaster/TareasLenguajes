var fs = require('fs');

function User (username, password) {
	this.username = username;
	this.password = password;
	this.current_dir = 'Usuarios/' + username;
	this.prev_dir = this.current_dir
}

User.prototype.changeDirectory = function (newDir) {
	ownDir = 'Usuarios/' + this.username;
	console.log('New dir' + newDir);
	
	if (new_dir == own_dir){
		console.log('Ya se encuentra en este directorio.');		
	}
	else if (new_dir == '..')
	{		
		this.current_dir = this.prev_dir;
		this.prev_dir = this.current_dir;
	}
	else
	{		
		fs.readdir(this.current_dir, function (err, files_dirs ){

		});

		el_dir = this.current_dir + '/' + new_dir;
		if (new_dir in files_dirs and os.path.isdir(el_dir)) {			
			this.prev_dir = this.current_dir;
			this.current_dir = this.prev_dir + '/' + new_dir;
		}
X
		for (var i = 0; i < files_dirs.length; i++) {
			console.log(files_dirs[i]);
		}
	}
}

User.prototype.listFiles = function () {
	
}

User.prototype.removeFile = function (filename) {
	
}

User.prototype.removeDirectory = function (dirname) {
	
}

User.prototype.createDirectory = function (dirname) {
	
}


User.prototype.getCurrentDirName = function () {
	
}