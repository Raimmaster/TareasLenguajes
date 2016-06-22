//libraries, vars
var fs = require('fs');//files
var net = require('net');//sockets
var readline = require('readline');//reading
var UserManager = require('./UserManager')
//port info
var HOST = '127.0.0.1';
var PORT = 8888;

var server = net.createServer();
server.listen(PORT, HOST);

//var wstream = fs.createWriteStream('');

console.log('Servidor en: ' + HOST + ':' + PORT)<
server.on('connection', (sock) => {
    console.log('Cliente conectado: ' + sock.remoteAddress + ':'
        + sock.remotePort);
    handleClient(sock);
});

const handleClient = (sock) => {
    var uManager = new UserManager();

    //client socket on
    sock.on('data', function(data){
        var message = JSON.parse(data);
        console.log(message);
        parseCommand(message,sock);

    });
    //client socket error
    sock.on('error', function(data){

    });
    //client socket closed
    sock.on('close', function(data){

    });
}

// message = {command, params[]}
const parseCommand = (message,sock) => {

    var command  = message.command;
    var data     = {};


    //****************************************
    //
    //
    //
    //TODO: Handle cases and response
    //
    //
    //
    //****************************************


    switch(command){
        case '1' :
            console.log('cd command handler');
            data.cd = 'I am random data';
            break;
        case '2' :
            //** example for ls command handle**
            console.log('ls command handler');
            // data.directories : data placeholder sent to client when ls is called
            // directories array content should be replaced  with what your user defined functons returns
            data.directories = ['foo','bar','chuck testa'];
            break;
        case '3' : console.log('put command handler');break;
        case '4' : console.log('get command handler');break;
        case '5' : console.log('rm command handler');break;
        case '6' : console.log('rmdir command handler');break;
        case '7' : console.log('mkdir command handler');break;
        case '8' : console.log('pwd command handler');break;
        case '9' : console.log('Exit command handler');break;
    }

    sendResponse({command,data},sock);
}

const sendResponse = (response, sock) => {
    sock.write(JSON.stringify(response));
};