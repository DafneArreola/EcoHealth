async function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });

    const result = await response.json();

    if (response.ok && result.success) {
        alert(result.message); // Show success message
        window.location.href = "/redirect-after-login"; // Redirect to home
    } else {
        alert(result.error); // Show error message
    }
}