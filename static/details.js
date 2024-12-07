// make copy icon copy the Email address
const $copyIcon = document.querySelector("#copyButton");

if ($copyIcon)
    $copyIcon.addEventListener('click', () => handleCopyClick());

const handleCopyClick = () => {
    const $email = document.querySelector("#copyEmail");
    const emailAddress = $email.innerText;
    navigator.clipboard.writeText(emailAddress);
}

// check validity of input field against HTML Email rule
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

// Open and close Email template modal
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
