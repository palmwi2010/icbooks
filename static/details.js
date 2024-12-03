// make copy icon work
const $copyIcon = document.querySelector("#copyButton");

if ($copyIcon)
    $copyIcon.addEventListener('click', () => handleCopyClick());

// submit button enabled when not empty
const $inputField = document.querySelector(".input-field");
const $submitButton = document.querySelector(".btn");

if ($inputField) {
    $inputField.addEventListener('input', (e) => checkValidity(e));
}

const checkValidity = (e) => {
    if (e.target.validity.patternMismatch) {
        e.target.setCustomValidity("Email must be a valid Imperial Email address.");
    } else {
        e.target.setCustomValidity("");
    }
}