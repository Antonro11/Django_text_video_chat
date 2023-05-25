        const senderVideo = document.getElementById('sender-video');
        const startButton = document.getElementById('start-button');
        const stopButton = document.getElementById('stop-button');
        const receiverContainer = document.getElementById('receiver-container');

        let senderStream;
        const receivers = new Map();

        // Access user media and set up sender video
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                senderStream = stream;
                senderVideo.srcObject = senderStream;
            })
            .catch(error => console.error('Error accessing user media:', error));

        // Start streaming
        startButton.addEventListener('click', () => {
            if (senderStream) {
                // Enable stop button and disable start button
                stopButton.disabled = false;
                startButton.disabled = true;

                // Create a new video element for the receiver
                const receiverVideo = document.createElement('video');
                receiverVideo.autoplay = true;
                receiverVideo.style.maxWidth = '200px';
                receiverContainer.appendChild(receiverVideo);

                // Create a new peer connection for the receiver
                const peerConnection = new RTCPeerConnection();
                receivers.set(receiverVideo, peerConnection);

                // Add sender stream to the peer connection
                senderStream.getTracks().forEach(track => peerConnection.addTrack(track, senderStream));

                // Create an offer and set as local description
                peerConnection.createOffer()
                    .then(offer => peerConnection.setLocalDescription(offer))
                    .then(() => {
                        // Send the offer to the receiver
                        const receiverOffer = {
                            sdp: peerConnection.localDescription.sdp,
                            type: peerConnection.localDescription.type
                        };
                        sendOfferToReceiver(receiverOffer);
                    })
                    .catch(error => console.error('Error creating offer:', error));
            }
        });

        // Stop streaming
        stopButton.addEventListener('click', () => {
            // Disable stop button and enable start button
            stopButton.disabled = true;
            startButton.disabled = false;

            // Close all peer connections and remove video elements
            receivers.forEach(peerConnection => {
                peerConnection.close();
            });
            receivers.clear();
            while (receiverContainer.firstChild) {
                receiverContainer.firstChild.remove();
            }
        });

        // Function to send offer to the receiver
        function sendOfferToReceiver(offer) {
            // Replace with your own logic to send the offer to the receiver
            // For example, using a WebSocket or a signaling server
            console.log('Sending offer to receiver:', offer);
        }