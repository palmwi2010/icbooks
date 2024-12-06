// make copy icon work
const $copyIcon = document.querySelector("#copyButton");

if ($copyIcon)
    $copyIcon.addEventListener('click', () => handleCopyClick());

// submit button enabled when not empty
const $inputField = document.querySelector(".input-field");

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

const handleCopyClick = () => {
    const $email = document.querySelector("#copyEmail");
    const emailAddress = $email.innerText;
    navigator.clipboard.writeText(emailAddress);
}

const $templateButton = document.querySelector("#email-template");
const $closeButton = document.querySelector("dialog button.primary");
const $modal = document.querySelector("dialog");

if ($templateButton) {
    $templateButton.addEventListener('click', e => {
        $modal.showModal();
    })

    $closeButton.addEventListener('click', (e) => {
        e.preventDefault();
        $modal.close();
    })
}
