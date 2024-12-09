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