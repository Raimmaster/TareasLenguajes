"use strict";
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
var loggedOptions =  ["\n","1. cd\n", "2. ls\n", "3. put (file)\n", "4. get\n", "5. rm file\n", "6. rmdir dir\n", "7. mkdir dir\n", "8. pwd\n", "9. Salir\n"];
var ori_menu = ["1. Crear usuario.", "2. Login.", "3. Salir."];
//var rdInput = readline.createInterface(process.stdin, process.stdout);

var client = new net.Socket();//client socket
var exit = false;
//self explanatory
client.connect(PORT, HOST, function() {
    console.log("Conectado : " + HOST + ':' + PORT);
    sendOption({message:'Hello server'});
    while(!exit){
    	inputOption();
    }
});

const sendOption = (data) => client.write(JSON.stringify(data));
const printMenu  = () => console.log(...loggedOptions);
//para recibir entradas, y devolver la opcion
const inputOption = () => {

	printMenu();

	var command = rl.question('Escribir opcion: ');
	var params = [];
	console.log("");
	switch(command){
		case "1": params[0] = c_cd();break;
		// no params for case 2 (ls)
		case "3": params    = c_put();break;
		case "4": params    = c_get();break;
		case "5": params[0] = c_rm();break;
		case "6": params[0] = c_rmdir();break;
		case "7": params[0] = c_mkdir();break;
		// no params for case 8 (pwd)
	}
	sendOption({command, params});
}

const c_cd     = () => rl.question('Ingrese directorio: ');
const c_rm     = () => rl.question('Nombre del archivo a remover: ');
const c_rmdir  = () => rl.question('Nombre del directorio a remover: ');
const c_mkdir  = () => rl.question('Nombre del directorio a crear: ');

const c_put = () => {
	var src       = rl.question('Nombre del archivo: ');
	var extension = rl.question('Extension: ');
	var dst       = rl.question('Destino del archivo: ') + extension;

	// TODO : Send stream of bytes
	var blob = "I am a stream of bytes";
	return [dst,blob];
};

const c_get = () => {
	var src       = rl.question('Nombre del archivo: ');
	var extension = rl.question('Extension: ');
	return [src,extension];
};


const createUser = function(client){
	var data;
	//get username
	data.usuario = rl.question('Ingrese el nombre de usuario: ');
	//get password
	data.password = rl.question('Ingrese el password: ');
	//send them both and get message
	var response = sendOption(data);
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