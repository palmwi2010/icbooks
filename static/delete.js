const $form = document.querySelector("form");
const $deleteBtns = document.querySelectorAll(".delete-btn");
const $input = document.querySelector("#book-id");

// when delete is pressed, send the form with the book id to delete
$deleteBtns.forEach($btn => {
    $btn.addEventListener('click', e => {
        $input.value = e.target.dataset.id;
        $form.submit();
    })
})

// hide the form until password is entered
$hiddenContent = document.querySelector(".hidden-content");
$hiddenContent.style.display="none";

// in practice password validation should happen at server
const password = "icbooks2425"

function checkPassword() {
    // Prompt user for password
    const userPassword = prompt("Enter the password to view admin services:");

    if (userPassword === null)
        return;

    if (userPassword === password) {
        $hiddenContent.style.display = "block";
    } else {
        alert("Incorrect password!");
        checkPassword();
    }
}

checkPassword();
