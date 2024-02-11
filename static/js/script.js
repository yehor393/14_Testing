document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Here you would handle the form submission, for example, using fetch to a backend server.
    console.log("Submitted with username:", username, "email:", email, "password:", password);

    // Example POST request (you will need to replace the URL with your actual backend endpoint)
    fetch('http://127.0.0.1:8000/users/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Handle success - maybe redirect to a login page or display a success message
    })
    .catch((error) => {
        console.error('Error:', error);
        // Handle errors, for example, show user an error message
    });
});
