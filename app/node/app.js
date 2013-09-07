var app = require('express')();
var server = require('http').createServer(app);
var io = require('socket.io').listen(server);

var redis = require("redis");
var client = redis.createClient();

server.listen(9000);

app.get('/', function(req, res){
    res.sendfile(__dirname + '/index.html');
});

client.select(1, function(err, res){
    if(err) return err;
    io.sockets.on('connection', function(socket){
        client.subscribe('proximos-trenes');
        client.on("message", function(channel, message){
            console.log('message:' + message);
            socket.emit('proximos trenes', message);
        });
    });
});
