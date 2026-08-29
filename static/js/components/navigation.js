// Variables
const menuButton = document.querySelector(".navbar__menu");
const sidebar = document.querySelector(".sidebar");
const closeButton = document.querySelector(".sidebar__close");

// Open Sidebar
function openSidebar(sidebar, menuBtn) {
    sidebar.classList.add("sidebar--open");
    menuBtn.setAttribute("aria-expanded", "true");
}

// Close Sidebar
function closeSidebar(sidebar, menuBtn) {
    sidebar.classList.remove("sidebar--open");
    menuBtn.setAttribute("aria-expanded", "false");
}

// Event Listeners
menuButton.addEventListener("click", () => {
    openSidebar(sidebar, menuButton);
});

closeButton.addEventListener("click", () => {
    closeSidebar(sidebar, menuButton);
});