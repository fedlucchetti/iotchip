'use strict';
var http = require('http');
//var Pusher = require('pusher');
var Pusher = require('pusher-client');
var fs = require('fs');
//var sys = require('sys')
var exec = require('child_process').exec;
var child;
/*
var pusher = new Pusher({
    appId: '194895',
    key: 'f3a6952cc326ee48eb10',
    secret: '700363677ba4fd2d6f8c',
    cluster: 'eu',
    encrypted: true
});
pusher.trigger('test_channel', 'my_event', { "message": "hello world" });
*/
var gotSerialNumber = false;
var serialnumber = "";

function excmd(cmd,msg) {
    console.log(msg);
    child = exec(cmd, function (error, stdout, stderr) {
        console.log('stdout: ' + stdout);
        console.log('stderr: ' + stderr);
        if (error !== null) {
            console.log('exec error: ' + error);
        }
    });
    return child;
}

child = exec("sudo python " + __dirname + "/beans/Microchip.py -n", function (error, serialnumber, stderr) {
    console.log('stdout: ' + serialnumber);
    gotSerialNumber = true;
    console.log(gotSerialNumber+":"+serialnumber);
    var pusher = new Pusher('f3a6952cc326ee48eb10', {
        cluster: 'eu'
    });
    serialnumber = serialnumber.replace(/^\s+|\s+$/g,'');
    serialnumber = serialnumber.replace(/\r?\n|\r/g,"");
    var my_channel = pusher.subscribe('channel_' + serialnumber);
    console.log("Pusher ready...");
    my_channel.bind('event_' + serialnumber, function (data) {
        console.log(data);
        if (gotSerialNumber) {

            /*
            for (var i = 0; i < 4; i++) {
                if (data.message == "fan_multipin_" + i + "_activity_on") {
                    excmd("sudo python " + __dirname + "/beans/FanController.py -s "+i,"Fan Multipin "+i+" On")
                }
                if (data.message == "fan_multipin_" + i + "_activity_off") {
                    excmd("sudo python " + __dirname + "/beans/FanController.py -h " + i, "Fan Multipin " + i + " Off")
                }
            }
            if (data.message == "fan_multipin_activity_on") {
                excmd("sudo python " + __dirname + "/beans/FanController.py -s 999", "Fan Multipin All On")
            }
            if (data.message == "fan_multipin_activity_off") {
                excmd("sudo python " + __dirname + "/beans/FanController.py -h 999", "Fan Multipin All Off")
            }
            */

            // ledsDict = { 0: 'red', 1: 'blue' }
            //for (var i in ledsDict) { // ledsDict[i]

            for (var i = 0; i < 2; i++) {
                if (data.message == "spotlight_multipin_" + i + "_activity_on") {
                    excmd("sudo python " + __dirname + "/beans/LedController.py -s " + i, "Spotlight Multipin " + i + " On")
                }
                if (data.message == "spotlight_multipin_" + i + "_activity_off") {
                    excmd("sudo python " + __dirname + "/beans/LedController.py -h " + i, "Spotlight Multipin " + i + " Off")
                }
            }
            if (data.message == "spotlight_multipin_activity_on") {
                excmd("sudo python " + __dirname + "/beans/LedController.py -s 999", "Spotlight Multipin All On")
            }
            if (data.message == "spotlight_multipin_activity_off") {
                excmd("sudo python " + __dirname + "/beans/LedController.py -h 999", "Spotlight Multipin All Off")
            }

        }
        //fs.writeFile("/home/pi/iotchip/logs/testNodePusher.json", JSON.stringify(data), function (err) {
        //   if (err) {
        //        return console.log(err);
        //    }
        //    console.log("The file was saved!");
        //});
    });
    if (error !== null) {
        console.log('exec error: ' + error);
        process.exit();
    }
});

http.createServer(function (req, res) {
    console.log(req.url);
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Hello Node.js\n');
}).listen(8124, "127.0.0.1");
console.log('Server running at http://127.0.0.1:8124/');
