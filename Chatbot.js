document.addEventListener('DOMContentLoaded', function() {
    var conversationHistory = [];

    var sendFunction = function() {
        var userInput = document.getElementById('userInput').value;
        var chatbox = document.getElementById('chatbox');
        chatbox.innerHTML += '<p>User: ' + userInput + '</p>';

        conversationHistory.push({ speaker: 'User', message: userInput });

        getChatbotResponse(userInput);
        document.getElementById('userInput').value = '';
        chatbox.scrollTop = chatbox.scrollHeight;
    };

    function getChatbotResponse(userInput) {
        var response;
        var lowerUserInput = userInput.toLowerCase();
        var responseMap = {
            hello: 'Hello!',
            hi: 'Hello!',
            hey: 'Hello!',
            howdy: 'Hello!',
            greetings: 'Hello!',
            goodbye: 'Goodbye!',
            bye: 'Goodbye!',
            name: 'My name is Chatbot.',
            default: 'I\'m sorry, I don\'t understand.'
        }

        for (var key in responseMap) {
            if (lowerUserInput.includes(key)) {
                response = responseMap[key];
                break;
            }
        }
    
        // Use the default response if no matching key is found
        response = response || responseMap.default;

        var chatbox = document.getElementById('chatbox');
        chatbox.innerHTML += '<p>Chatbot: ' + response + '</p>';

        conversationHistory.push({ speaker: 'Chatbot', message: response });
    }

    // Additional code for displaying conversation history
    function displayConversationHistory() {
        var chatbox = document.getElementById('chatbox');
        chatbox.innerHTML = '';

        for (var i = 0; i < conversationHistory.length; i++) {
            var message = conversationHistory[i];
            chatbox.innerHTML += '<p>' + message.speaker + ': ' + message.message + '</p>';
        }

        chatbox.scrollTop = chatbox.scrollHeight;
    }

    // Attach sendFunction to the "Send" button
    document.getElementById('sendButton').addEventListener('click', sendFunction);
    document.addEventListener('enter', sendFunction);
});