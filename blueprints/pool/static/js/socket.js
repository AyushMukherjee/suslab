var socket = io();
    socket.on('pool', function(message, json) {
        console.log(message)
        console.log('Received '+Object.keys(json.data).length+' elements.')
    });