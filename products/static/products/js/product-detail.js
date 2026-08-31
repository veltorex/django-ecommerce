// Variables
const prevButton = document.getElementById("prev-btn");
const nextButton = document.getElementById("next-btn");
const product = document.querySelector(".product__image-container");
const productImage = document.querySelector(".product__image");

const images = JSON.parse(product.dataset.images);

let currentIndex = 0;

// Previous
prevButton.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    productImage.src = images[currentIndex];
});

// Next
nextButton.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % images.length;
    productImage.src = images[currentIndex];
});