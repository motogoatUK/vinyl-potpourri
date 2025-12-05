//**
// autocomplete.js - put together after a lot of searching and trying to get 
// django-autocomplete-light working
// code: a combination of my own code, Bing, co-pilot and chatGPT 
// Given more time I'm sure my own code could have worked! 
// > 12/12/25 - SD.Thornes
// added code for keyboard navigation
// refactored to use any fk (e.g artist and location)
// */
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("input.autocomplete").forEach((input) => {
        // changed consts to use data-urls for universal use
        const url = input.dataset.url;
        const hidden = document.querySelector(input.dataset.target);

        let box = null;
        let activeIndex = -1;
        let items = [];

        function closeBox() {
            if (box) box.remove();
            box = null;
            items = [];
            activeIndex = -1;
            input.classList.remove("autocomplete-open");
        }

        function highlightItem(index) {
            items.forEach((el, i) => {
                el.classList.toggle("active", i === index);
            });
        }

        input.addEventListener("input", async () => {
            const q = input.value;
            hidden.value = ""; // clear old value

            if (q.length < 2) {
                closeBox();
                return;
            }

            const resp = await fetch(url + "?q=" + encodeURIComponent(q));
            const results = await resp.json();

            closeBox();
            box = document.createElement("div");
            box.classList.add("autocomplete-box");
            input.after(box);
            input.classList.add("autocomplete-open");

            items = results.map((item, index) => {
                const option = document.createElement("div");
                option.textContent = item.name;

                option.addEventListener("click", () => {
                    input.value = item.name;
                    hidden.value = item.id;
                    closeBox();
                });

                box.appendChild(option);
                return option;
            });
        });
// Add code for keyboard use
        input.addEventListener("keydown", (event) => {
            if (!box) return;

            switch (event.key) {
                case "ArrowDown":
                    event.preventDefault();
                    activeIndex = (activeIndex + 1) % items.length;
                    highlightItem(activeIndex);
                    break;

                case "ArrowUp":
                    event.preventDefault();
                    activeIndex = (activeIndex - 1 + items.length) % items.length;
                    highlightItem(activeIndex);
                    break;

                case "Enter":
                    if (activeIndex >= 0) {
                        event.preventDefault();
                        items[activeIndex].click();
                    }
                    break;

                case "Escape":
                    closeBox();
                    break;
            }
        });
  // chatGPT helped here
        document.addEventListener("click", (e) => {
            if (box && !box.contains(e.target) && e.target !== input) {
                closeBox();
            }
        });
    });
});
