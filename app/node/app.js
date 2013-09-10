var io = require('socket.io').listen(9000);

var redis = require("redis");
var client = redis.createClient();

client.select(1, function(err, res){
    if(err) return err;
    io.sockets.on('connection', function(socket){
        client.subscribe('proximos-trenes');
        client.on("message", function(channel, message){
            socket.emit('proximos trenes', JSON.parse(message));
        });
    });
});
