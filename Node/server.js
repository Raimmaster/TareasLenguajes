//libraries, vars
var fs = require('fs');//files
var net = require('net');//sockets
var readline = require('readline');//reading
var userManager = require('./UserManager')
//port info
var HOST = '127.0.0.1';
var PORT = 8888;

var server = net.createServer();
server.listen(PORT, HOST);

var wstream = fs.createWriteStream('');

console.log('Servidor en: ' + HOST + ':' + PORT)<

server.on('connection', function(sock) {
    console.log('Cliente conectado: ' + sock.remoteAddress + ':' 
        + sock.remotePort);
    handleClient(sock);
});

var handleClient = function(sock) {
    var uManager = new UserManager();

    //client socket on
    sock.on('data', function(data){

    });
    //client socket closed
    sock.on('close', function(data){

    });
    //client socket error
    sock.on('error', function(data){

    });
}
