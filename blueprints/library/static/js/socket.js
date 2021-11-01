var socket = io();
    socket.on('library', function(message) {
        console.log(message)
    });