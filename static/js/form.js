function clickButtonPassword(element) {
    const inputPassword = element.previousElementSibling;
    const showPasswordIcon = element.firstElementChild;
    const hidePasswordIcon = element.lastElementChild;
    
    if (inputPassword.type === "password") {
        inputPassword.type = "text";
        showPasswordIcon.classList.add("hidden");
        hidePasswordIcon.classList.remove("hidden");
    } else {
        inputPassword.type = "password";
        showPasswordIcon.classList.remove("hidden");
        hidePasswordIcon.classList.add("hidden");
    }
};