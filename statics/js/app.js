$(document).ready(function() {
    var messageForm = $('#form .message');
    var timeline = $('#timeline .messages');
    function addMessage(date, text) {
        let messageLine = $('<li/>')
        messageLine.text(date.toUTCString() + ': ' + text);
        timeline.prepend(messageLine);
    }
    var isClosed = true;
    function open() {
        ws = new WebSocket('ws://127.0.0.1:8080/chat');
        ws.onopen = function(e) {
            isClosed = false;
            addMessage(new Date(), 'start');
            ws.send('Hello!')
        };
        ws.onmessage = function(e) {
            addMessage(new Date(),e.data);
        };
        ws.onclose = function(e) {
            isClosed = true;
            addMessage(new Date(), 'close');
        };
        $('#form button').click(function(){
            let text = messageForm.val();
            ws.send(text);
            messageForm.val('');
        })
    }
    (function autoopen() {
        if (isClosed) {
            open();
        }
        setTimeout(autoopen, 5000);
    })();
});
