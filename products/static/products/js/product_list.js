const filterButton = document.querySelector(".product-list__open-filters-list")
const filterSidebar = document.querySelector(".mobile-filters")

// Events
filterButton.addEventListener("click", () => {
    // Hide or show filter sidebar
    filterSidebar.classList.toggle("hidden")
})