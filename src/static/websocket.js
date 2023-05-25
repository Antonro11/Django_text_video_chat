 const groupName = document.getElementById('chat_room');
    console.log(groupName)
const socket = new WebSocket('ws://127.0.0.1:8000/ws/chat/'+groupName+'/');

socket.onopen = (event) => {
    // Handle WebSocket connection opened
    console.log('WebSocket connection opened:', event);

    // Send a message after the connection is opened
    socket.send(JSON.stringify({'message': 'Hello, world!'}));
};

socket.onmessage = (event) => {
  // Handle received message
  const receivedMessage = JSON.parse(event.data).message;
  displayMessage(receivedMessage);
};

function sendMessage() {
  // Get the message input value
  const message = document.getElementById('messageInput').value;
  // Send the message as a WebSocket message
  socket.send(JSON.stringify({ message: message }));
  // Display the sent message in the chat box
  displayMessage(`You: ${message}`);
  // Clear the message input
  document.getElementById('messageInput').value = '';
}

function displayMessage(message) {
  // Create a new paragraph element to display the message
  const newMessage = document.createElement('p');
  newMessage.innerText = message;
  // Append the paragraph element to the chat box
  document.getElementById('chatBox').appendChild(newMessage);
}



socket.onclose = (event) => {
    // Handle WebSocket connection closed
    console.log('WebSocket connection closed:', event);
};