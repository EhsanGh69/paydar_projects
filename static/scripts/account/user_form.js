$(document).ready(function () {
    // password
    const passwordField = document.getElementById("id_password");
    const togglePassword = document.querySelector("#password-toggle-icon");

    togglePassword.addEventListener("click", function () {
    if (passwordField.type === "password") {
        passwordField.type = "text";
        togglePassword.classList.remove("fa-eye");
        togglePassword.classList.add("fa-eye-slash");
    } else {
        passwordField.type = "password";
        togglePassword.classList.remove("fa-eye-slash");
        togglePassword.classList.add("fa-eye");
    }
    });

    // confirm password
    const confirmPasswordField = document.getElementById("id_confirm_password");
    const toggleConfirmPassword = document.querySelector("#confirm-toggle-icon");

    toggleConfirmPassword.addEventListener("click", function () {
    if (confirmPasswordField.type === "password") {
        confirmPasswordField.type = "text";
        toggleConfirmPassword.classList.remove("fa-eye");
        toggleConfirmPassword.classList.add("fa-eye-slash");
    } else {
        confirmPasswordField.type = "password";
        toggleConfirmPassword.classList.remove("fa-eye-slash");
        toggleConfirmPassword.classList.add("fa-eye");
    }
    });

});