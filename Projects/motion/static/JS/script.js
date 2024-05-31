 
function sendButtonId(buttonId) {
    console.log("Button ID: " + buttonId);
 
    // Veriyi Flask'a gönder
    fetch('/route', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ buttonId: buttonId })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}