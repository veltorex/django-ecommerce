// Elements
const filterButton = document.querySelector(".product-list__open-filters-list")
const filterSidebar = document.querySelector(".mobile-filters")
const filterClose = document.querySelector(".mobile-filters__close")

// Events
filterButton.addEventListener("click", () => {
    // Hide or show filter sidebar
    filterSidebar.classList.toggle("hidden")

    // Disable or enable scrolling
    document.body.classList.toggle("no-scroll")
})

filterClose.addEventListener("click", () => {
    // Hide filter sidebar
    filterSidebar.classList.add("hidden")

    // Allow scrolling
    document.body.classList.remove("no-scroll")
})