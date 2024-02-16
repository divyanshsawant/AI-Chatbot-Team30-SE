const password_input = document.querySelector("#password_input");
const password_eye = document.querySelector("#password_eye");


password_eye.addEventListener('click', () => {
    if (password_input.type == "password") {
        password_input.type = "text";
        password_eye.classList.add("fa-eye");
        password_eye.classList.remove("fa-eye-slash");


    } else if (password_input.type == "text") {
        password_input.type = "password";
        password_eye.classList.add("fa-eye-slash");
        password_eye.classList.remove("fa-eye");
    }

});
