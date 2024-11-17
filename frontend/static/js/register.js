async function handleRegister(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const email = document.getElementById("email").value;

    const response = await fetch("/api/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password, email })
    });

    const result = await response.json();

    if (response.ok && result.success) {
        alert(result.message); // Show success message
        window.location.href = "/redirect-after-register"; // Redirect to login
    } else {
        alert(result.error); // Show error message
    }
}