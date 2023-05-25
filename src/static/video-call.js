console.log("Second account vid",secondUserVideo)
console.log("Hello from main 2 !")
console.log("Who start stream: ",whoStartStream)


const videosDiv = document.getElementById('videos');
const localVideo = document.getElementById('local-video');
const remoteDiv = document.getElementById('remote-videos')
const startButton = document.getElementById('start-button');
const stopButton = document.getElementById('stop-button');
const turnOffVideo = document.getElementById('turn-off-video')
onmessageStart = 0

var turnOnVideoButton = document.createElement("button")
turnOnVideoButton.textContent = "Turn on camera"

const remoteVideo = document.createElement('video');


let servers = {
    iceServers:[
        {
            urls:['stun:stun1.1.google.com:19302', 'stun:stun2.1.google.com:19302']
        }
    ]
}




const websocket = new WebSocket('ws://' + window.location.host + '/ws/video-chat/' + chatRoom + '/');
const peerConnection = new RTCPeerConnection(servers);

let userMediaStream = new MediaStream();


const videoConstraintsMinim = {
  audio: false,
  video: {
    width: { max: 5 },
    height: { max: 5 },
    frameRate: { max: 1 },
  }
};


async function takeMedia() {
                if (user != "some_user") {
         userMediaStream = await navigator.mediaDevices.getUserMedia({
              audio: true,
              video: true
            });   } else {userMediaStream = await navigator.mediaDevices.getUserMedia(videoConstraintsMinim)}

             userMediaStream.getTracks().forEach(track => {
             peerConnection.addTrack(track, userMediaStream);
                     });
             localVideo.srcObject = userMediaStream;

    }







async function sendOffer() {
        const offer = await peerConnection.createOffer()

        peerConnection.setLocalDescription(offer);
        websocket.send(JSON.stringify({
            peer:user,
            event:"offer",
            data:offer
        }))
       }


async function sendCandidate() {
          peerConnection.onicecandidate = event => {
            websocket.send(JSON.stringify({
            peer:user,
            event:"candidate",
            data:event.candidate
        }))
        }
    }


async function listenTrackToRemote() {
                  peerConnection.addEventListener('track', event => {
                   remoteVideo.autoplay = true;
                    console.log('Got remote stream',event);
                    remoteStream = event.streams[0];
                    remoteVideo.srcObject = remoteStream;
                    remoteDiv.appendChild(remoteVideo)
                  });
            }

function stopMedia() {

               const audioTracks = userMediaStream.getAudioTracks();
              videoCapture = localVideo.srcObject

                const videoTracks = userMediaStream.getVideoTracks();
                for (const track of audioTracks) {
                  track.stop();
                }
                for (const track of videoTracks) {
                  track.stop();
                }
            }





  websocket.onopen = async (event) => {
        console.log("Websocket connection opened...")
        websocket.send(JSON.stringify({"user_connected":user}))
        websocket.send(JSON.stringify({"first_click":user}))
        sendOffer();sendCandidate();takeMedia();listenTrackToRemote();startButton.remove()
                }





websocket.onmessage =async (event) => {

        console.log("Websocket onmessage... ")

    if (remoteVideo.srcObject == null ) {console.log("remoteSRC ------> ",remoteVideo.srcObject),localVideo.className = ""}


    if (remoteVideo.style.display != "none") {if (remoteVideo) {localVideo.classList.add("local-video")}} else {localVideo.classList.remove("local-video"); remoteVideo.style = "display:none"}

        var content = JSON.parse(event.data)
        var data = content.data.data


        if (content.data.event == "close-video") {stopMedia();window.location.href = "http://localhost:8000/app/chat/"+ chatRoom+"/";}

        if (content.data.event == "turn_off_video") {if (user == content.data.peer) {
              stopMedia()
        } else {remoteVideo.style = "visibility:hidden";remoteVideo.style = "display:none";localVideo.classList.remove("local-video")}}

        if (content.data.event == "turn_on_video") {if (user == content.data.peer) {
        takeMedia(); if (remoteVideo.style.visibility == "hidden") {localVideo.classList.remove("local-video")}
        } else {remoteVideo.style = "visibility: visible;";listenTrackToRemote();localVideo.classList.add("local-video")}};


        whoStartStream = content.data.first_click
        userConnected = content.data.user_connected



        if (content.data.peer === user) {return;}

 switch (content.data.event) {
        case ("offer"):

            console.log("answer on offer")

            peerConnection.setRemoteDescription(data)

            const answer = await peerConnection.createAnswer();
            console.log("Answer:",answer)

            await peerConnection.setLocalDescription(answer)
            websocket.send(JSON.stringify({
                peer:user,
                event:"answer",
                data:answer
            }))

            break;

        case ("answer"):
            console.log("answer on answer")
            await peerConnection.setRemoteDescription(data)

            break;

        case ("candidate"):
            console.log("answer on candidate")
            peerConnection.addIceCandidate(data)
            break;

        case ("cancel-call"):
            window.location.href = "http://localhost:8000/app/chat/"+ chatRoom+"/";

    }
};


websocket.onclose = (event) => {
        stopMedia()
        console.log("Websocket closed...")
};


takeMedia();listenTrackToRemote();startButton.remove()

localVideo.muted = true;


stopButton.addEventListener("click", () => {
    websocket.send(JSON.stringify({event:"close-video",peer:user}))
})

turnOffVideo.addEventListener("click", () => {

           websocket.send(JSON.stringify({
            peer:user,
            event:"turn_off_video",
        }))

        videosDiv.appendChild(turnOnVideoButton)
        turnOffVideo.remove()
        localVideo.srcObject = null
        localVideo.style = "visibility: hidden;"
})


turnOnVideoButton.addEventListener("click", () => {

   if (remoteVideo.style.visibility == "hidden") {console.log("Hidden statement");
            while (localVideo.classList.length > 0) {
  localVideo.classList.remove(localVideo.classList.item(0));
}
        }

   listenTrackToRemote();

          websocket.send(JSON.stringify({
            peer:user,
            event:"turn_on_video",
        }))

        localVideo.style = "visibility: visible;"
        localVideo.muted = true;
        videosDiv.appendChild(turnOffVideo)
        turnOnVideoButton.remove()
            })
