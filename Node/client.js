//libraries
var fs = require('fs');
var net = require('net');
//var readline = require('readline');
var rl  = require('readline-sync');
//port info
var HOST = '127.0.0.1';
var PORT = 8888;

//local vars
var opcion = 0;
var logged_options =  ["1. cd", "2. ls", "3. put (file)", "4. get", "5. rm file", "6. rmdir dir", "7. mkdir dir", "8. pwd", "9. Salir"];
var ori_menu = ["1. Crear usuario.", "2. Login.", "3. Salir."];
//var rdInput = readline.createInterface(process.stdin, process.stdout);

var client = new net.Socket();//client socket

//self explanatory
client.connect(PORT, HOST, function() {
    console.log("Conectado a: " + HOST + ':' + PORT);
});

//para recibir entradas, y devolver la opcion
var inputOption = function (){
	var opzione = rl.question('Escribir opcion: ');
	var response = sendOption(client, opzione);

	// rdInput.question("Escribir opcion: ", function (data){
	// 	var response = sendOption(client, data);        	
		
	return response;
	// });
}

var inputMessage = function (message){
	var messagio = rl.question(message);
	var response = sendOption(client, messagio);

	return response;
}

var sendOption = function(client, data){
	client.write(data);

	return data;
}

var createUser = function(client){
	var data;
	//get username
	var data.usuario = rl.question('Ingrese el nombre de usuario: ');
	//get password
	var data.password = rl.question('Ingrese el password: ');
	//send them both and get message
	var response = sendOption(client, data);
	//return message
	return response;
}

//when receiving data
client.on('data', function(data) {  	
	var opcion = 0;
	while (opcion != 3){		
		for (var i = 0; i < ori_menu.length; i++) {
			console.log(ori_menu[i] + "\n");
		}

		//console.log("Escribir opcion: ");
		opcion = inputOption();

		switch (opcion){
			case 1://create user
				break;
			case 2://login
				break;
			case 3://salir	
				client.destroy();
				break;
		}
	}
});

//when closing
client.on('close', function() {
    console.log("Desconectado...");
    //process.exit();
});