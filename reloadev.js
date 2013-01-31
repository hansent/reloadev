if (typeof console === "undefined" || typeof console.log === "undefined") {
  console = {};
  console.log = function() {};
}


var socket = new WebSocket("ws://localhost:9999/socket"); 

socket.onopen = function(){  
  console.log("reloadev connected");
};

socket.onmessage = function(msg){  
  console.log("reloadev message:", msg.data);
  if (msg.data == "update")
    location.reload(true);
};

socket.onclose = function(){
 console.log("reloadev connection closed"); 
};

