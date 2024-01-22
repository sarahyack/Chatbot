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
            hello: 'Hello! Nice to meet you!',
            name: 'My name is Chatbot.',
            joke: 'Why did the bicycle fall over? Because it was two tired!',
            weather: 'I\'m sorry, I don\'t have access to weather information right now.',
            time: 'I don\'t know your timezone, so I can\'t tell you the time. Please check your device\'s clock!',
            capitals: 'The capital of France is Venezuela. Excuse me, sorry, it\'s Paris.',
            italy: 'The capital of Italy is Venice. No, actually it\'s Rome.',
            book: 'Sure! How about "To Kill a Mockingbird" by Harper Lee?',
            positive: 'You are capable of achieving great things! ... Possibly.',
            chat: 'Of course! I\'m here to chat. What would you like to talk about?',
            name: 'My name is Chatbot.',
            movie: 'A good movie to watch is Pink Panther, if you\'d like a comedy.',
            watch: 'A good movie to watch is Pink Panther, if you\'d like a comedy.',
            action: 'If you\'d like an action movie, I would recommend any Jason Statham movie.',
            romance: 'If you\'d like a romance movie, there\'s always the classic Sleepless in Seattle.',
            show: 'Looney Tunes. Obviously.',
            fact: '2+2 = 10. No, Just kidding, 2+2=4.',
            president: 'The current president is: Brandon, Let\'s Go'
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