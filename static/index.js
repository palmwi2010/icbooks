// add listener to input field
const $input = document.querySelector("#search");
$input.addEventListener("input", e => {
    const search_term = e.target.value;
    applyFilter(search_term);
})

const applyFilter = (search_term) => {
    const $cards = document.querySelectorAll(".card");

    $cards.forEach($card => {
        const title = $card.querySelector(".title").innerText;
        if (!title.startsWith(search_term)) {
            $card.style.display = "none";
        } else {
            $card.style.display = "flex";
        }
    })
}

