  console.log(window.location.host)

    var button = document.getElementById("myButton");
    var textInput = document.getElementById("textInput");
    var myDiv = document.getElementById("myDiv");
    var videoCallButton = document.getElementById("video-call");
    var divCallStatus = document.getElementById("div-call-status");
    var indexDelete = 0;
    var chatContent = document.getElementById("chat-content");


    textInput.style.cssText = 'height: ${textInput.scrollHeight}px;overflow-y:hidden; width:250px;'

    textInput.addEventListener("input", function() {
            this.style.height = "auto"
            this.style.height = '${this.scrollHeight}px'
    })





var image ="{% static 'x-delete-button-png-14.png' %}"


var paragraph = document.createElement("p");




   const socket = new WebSocket('ws://'+ window.location.host +'/ws/chat/'+chatRoom+'/');
   const ws = new WebSocket('ws://'+ window.location.host + '/ws/list/1/');
   const websocket = new WebSocket('ws://' + window.location.host + '/ws/video-chat/'+chatRoom +"/");
   const socketStatusCall = new WebSocket('ws://' + window.location.host + '/ws/calling-status/'+chatRoom +"/" + user + "/");



textInput.addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight + 2) + 'px';
  this.scrollTop = this.scrollHeight;
});



myDiv.scrollTop = myDiv.scrollHeight;



      button.addEventListener("click", function() {
      text = textInput.value;

      socket.send(JSON.stringify({
      "user":user,
      "text":text
      }));
      textInput.value = ""
      textInput.style.cssText = 'height: ${textInput.scrollHeight}px;overflow-y:hidden; width:250px;'
    });



          videoCallButton.addEventListener("click", function() {
            // event.preventDefault();
          socket.send(JSON.stringify({'video-call-clicked':user}))
          ws.send(JSON.stringify({'video-call-clicked':user,"room":chatRoom}))
          socketStatusCall.send(JSON.stringify({'video-call-clicked':user}))
                })


function AjaxRequest(deleteValue) {


       fetch("/app/chat/"+chatRoom+"/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ delete_index: deleteValue })
      })
      .then(response => {
        console.log("Message deleted successfully.");
        location.reload()
      })
      .catch(error => {
        console.error("Error deleting message:", error);
      });
}





function AllMessagesList() {
for (let i = 0; i < allMessages.length; i++) {
  const fullMessage = allMessages[i];
  userMessage = fullMessage.split("__split__")[0]
  textMessage = fullMessage.split("__split__")[1]
  messageElement = document.createElement("p")
  messageElement.textContent = userMessage+": "+textMessage

        messageElement.id = i

      if (userMessage == user) {messageElement.style ="position:relative; left:50%;color:green;";
                    var buttonDelete = document.createElement("button")

                    buttonDelete.style = "position:relative;height:15px;width:15px; right:-10px; top:3px;border:blue;"
                    buttonDelete.style.backgroundImage = 'url(http://' + window.location.host + '/static/x-delete-button-png-14.png)'
                    buttonDelete.style.backgroundPosition = "center";
                    buttonDelete.style.backgroundSize = "cover";
                    buttonDelete.type = "button"
                    buttonDelete.id = i

                    indexDelete = i
                    buttonDelete.value = indexDelete

                   buttonDelete.onclick = function() {
                   socket.send(JSON.stringify({"reload_after_delete":i,"peer":user}))
                    AjaxRequest(i);
                  };
                    messageElement.appendChild(buttonDelete)
                    }

      else {messageElement.style ="position:relative; right:30%;color:black;"}
        chatContent.appendChild(messageElement)
    }
   }


AllMessagesList()


socket.onopen = (event) => {
        socket.send(JSON.stringify({"ws_opened":user}))
        console.log("Websocket connection opened...")
        myDiv.scrollTop = myDiv.scrollHeight;
}


socket.onmessage = (event) => {
    console.log("Websocket onmessage...")
    var data = JSON.parse(event.data);
   var message = data.message;
   var wsOpened = data.ws_opened
   var videoClicked = data.clicked
   var reloadDelete = data.reload_after_delete
   var allMessages = data.all_messages;
  //  console.log("Data",data)


    if (reloadDelete) {
            if (user != reloadDelete.peer) {location.reload()}
            }


    if (wsOpened) {console.log("Ws opened....")}


    if(videoClicked) {

        if (user != videoClicked["video-call-clicked"]) {
        window.location.href = 'http://' + window.location.host + '/app/calling-status/'+ chatRoom+"/"+videoClicked["video-call-clicked"]+"/"}

        var newElement = document.createElement("h2")
        var audioElement = document.createElement("audio")
        var buttonAnswerCall = document.createElement("button")
        var buttonCancelCall = document.createElement("button")

        buttonAnswerCall.textContent = "Answer"
        buttonCancelCall.textContent = "Cancel"


        audioElement.src = 'http://' + window.location.host + '/static/telephone-ring-04.mp3'
            audioElement.autoplay = true
        newElement.textContent = videoClicked["video-call-clicked"] + " is calling"
        divCallStatus.appendChild(newElement)
        divCallStatus.appendChild(buttonAnswerCall)
        divCallStatus.appendChild(buttonCancelCall)
        newElement.appendChild(audioElement)

         buttonCancelCall.addEventListener("click", function() {
            websocket.send(JSON.stringify({"event":"cancel-call"}))
            location.reload();
                    })

         buttonAnswerCall.addEventListener("click", function() {
            window.location.href = 'http://' + window.location.host + '/app/video-chat/'+ chatRoom+"/";
                })
    }

    if (message) {
        messageElement = document.createElement("p")
        messageElement.textContent = message.user +": " + message.text

            indexDelete ++
            messageElement.id = indexDelete

             if (message.user == user) {messageElement.style ="position:relative; left:50%;color:green;"
                    var buttonDelete = document.createElement("button")

                    buttonDelete.style = "position:relative;height:15px;width:15px; right:-10px; top:3px;border:blue;"
                    buttonDelete.style.backgroundImage = 'url(http://' + window.location.host + '/static/x-delete-button-png-14.png)'
                    buttonDelete.style.backgroundPosition = "center";
                    buttonDelete.style.backgroundSize = "cover";
                    buttonDelete.type = "button"



                    buttonDelete.id = indexDelete
                    console.log(buttonDelete.id)



                   buttonDelete.onclick = function() {
                   socket.send(JSON.stringify({"reload_after_delete":indexDelete,"peer":user}))
                   AjaxRequest(indexDelete);
                  };

            messageElement.appendChild(buttonDelete)

             }
             else {messageElement.style ="position:relative; right:30%;color:black;"}
        ws.send(JSON.stringify({"update_from_room": chatRoom}))
        chatContent.appendChild(messageElement)
    }

myDiv.scrollTop = myDiv.scrollHeight;
};


socket.onclose = (event) => {
    console.log('WebSocket connection closed',event);
};

