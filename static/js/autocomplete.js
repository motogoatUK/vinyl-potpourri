//**
// autocomplete.js - put together after a lot of searching and trying to get 
// django-autocomplete-light working
// code: a combination of my own code, Bing, co-pilot and chatGPT 
// Given more time I'm sure my own code could have worked! 
// */
document.addEventListener("DOMContentLoaded", () => {
    const input = document.querySelector("#id_artist_name");
    const hidden = document.querySelector("#id_artist_id");
    let box = null;

    input.addEventListener("input", async () => {
        const q = input.value;
        hidden.value = ""; // clear selected ID

        if (q.length < 2) {
            if (box) box.remove();
            input.classList.remove("autocomplete-open");
            return;
        }

        const resp = await fetch(`/record/artist-autocomplete/?q=${encodeURIComponent(q)}`);
        const results = await resp.json();

        if (box) box.remove();
        box = document.createElement("div");
        box.classList.add("autocomplete-box");

        results.forEach(item => {
            const option = document.createElement("div");
            option.textContent = item.name;
            option.addEventListener("click", () => {
                input.value = item.name;
                hidden.value = item.id;
                box.remove();
                input.classList.remove("autocomplete-open");
            });
            box.appendChild(option);
        });

        input.after(box);
        input.classList.add("autocomplete-open");
    });

    // Hide dropdown when clicking outside
    document.addEventListener("click", e => {
        if (box && !box.contains(e.target) && e.target !== input) {
            box.remove();
            input.classList.remove("autocomplete-open");
        }
    });
});