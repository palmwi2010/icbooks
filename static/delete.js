const $form = document.querySelector("form");
const $deleteBtns = document.querySelectorAll(".delete-btn");
const $input = document.querySelector("#book-id");


$deleteBtns.forEach($btn => {
    $btn.addEventListener('click', e => {
        $input.value = e.target.dataset.id;
        $form.submit();
    })
})