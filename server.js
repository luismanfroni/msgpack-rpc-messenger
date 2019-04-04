const readlineSync = require('readline-sync');
const spawn = require('threads').spawn;
const rpc = require('framed-msgpack-rpc');

const thread = spawn(function(input, done) {
    var rpc = require('framed-msgpack-rpc');
    var address;
    var lobby = input.lobby;
    var name;

    function sendMessage(message) {

    }

    console.log(input.ip, input.port)

    var srv= new rpc.Server ({
        programs : {
            "messenger" : {
                connect : (arg, response) => {
                    try {
                        var x = rpc.createTransport({ host: arg.ip, port : arg.port });
                        x.connect(function (err) {
                            var c = new rpc.Client(x, "messenger");
                            c.invoke('connectSuccess', {}, function(err, response) {
                                if (err) {
                                    console.log("error in RPC: " + err);
                                } else { 
                                    if(response) {
                                        lobby.push([arg.ip, arg.port]);
                                        done({ lobby: lobby });
                                    }
                                }
                                x.close();
                            });
                        })
                       
                        lobby.push([arg.ip, arg.port]);
                        done({ lobby: lobby });
                        response.result(true);
                    } catch (error) {
                        response.result(false);
                    }
                },
                connectSuccess: (arg, response) => {
                    response.result(true);
                },
                getLobby: (arg, response) => {
                    response.result(lobby);
                },
                receiveMessage: (arg, response) => {
                    console.log(arg.name, ":", arg.message);
                    response.result('success');
                }
            }
        },
        port : input.port 
    });

    srv.listen(function (err) {
        if (err) {
            console.log("Error binding: " + err);
        } else {
            console.log("Listening!");
        }
    });
  });

var lobby = [];
var port = readlineSync.question('port: ');
thread.send({ip:'127.0.0.1', port: port, lobby: lobby})
.on('message', function(response) {
    lobby = response.lobby
})


while(true) {
    var message = readlineSync.question('Send: ');
    lobby.forEach((address) => {
        var x = rpc.createTransport({ host: address[0], port : address[1] });
        x.connect(function (err) {
            if (err) {
                console.log("error connecting");
            } else {
                var c = new rpc.Client(x, "messenger");
                c.invoke('receiveMessage', { name : 'lucas', message : message}, function(err, response) {
                    if (err) {
                        console.log("error in RPC: " + err);
                        let i = lobby.findIndex((a) => a[0] === address[0] && a[1] === address[1])
                        lobby.splice(i, 1);
                    } else { 
                        console.log(response)
                    }
                    x.close();
                });
            }
        });
    })
}