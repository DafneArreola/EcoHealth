document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.querySelector('.login-btn');
    loginBtn.addEventListener('click', () => {
        alert('Redirecting to login page...');
        // Redirect to login page
        window.location.href = '/login';
    });
});
