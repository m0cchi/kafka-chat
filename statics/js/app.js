$(document).ready(function() {
    var messageForm = $('#form .message');
    var timeline = $('#timeline .messages');
    function addMessage(date, text) {
        let messageLine = $('<div/>')
        let field = $('<div/>');
        if(text.toLowerCase().match(/^http.*(png|jpeg|jpg|gif)$/)) {
            field.text(date.toUTCString() + ': ');
            messageLine.append(field);
            let img = $('<img/>');
            img.attr('src', text);
            messageLine.append(img);
        } else {
            field.text(date.toUTCString() + ': ' + text);
            messageLine.append(field);
        }

        timeline.prepend(messageLine);
    }

    ws = new WebSocket('ws://127.0.0.1:8080/chat');
    ws.onopen = function(e) {
        addMessage(new Date(), 'start');
        ws.send('Hello!')
    };
    ws.onmessage = function(e) {
        addMessage(new Date(),e.data);
    };
    ws.onclose = function(e) {
        addMessage(new Date(), 'close');
    };
    $('#form button').click(function(){
        let text = messageForm.val();
        ws.send(text);
        messageForm.val('');
    })
});
