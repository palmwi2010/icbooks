// add listener to input field
const $input = document.querySelector("#search");
$input.addEventListener("input", e => {
    const search_term = e.target.value;
    applyFilter(search_term);
})

const applyFilter = (search_term) => {
    const $cards = document.querySelectorAll(".card");

    // case insensitive: take lower
    const search_lower = search_term.toLowerCase();

    $cards.forEach($card => {
        const title = $card.querySelector(".title").innerText;
        const title_lower = title.toLowerCase(); // case insensitive

        if (!title_lower.startsWith(search_lower)) {
            $card.style.display = "none";
        } else {
            $card.style.display = "flex";
        }
    })
}

