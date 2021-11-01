var socket = io();
    socket.on('pool', function(message) {
        console.log(message)
    });