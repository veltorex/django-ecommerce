const imageForms = document.querySelectorAll(".image-form");

imageForms.forEach((form, index) => {
    const input = form.querySelector('input[type="file"]');
    const deleteButton = form.querySelector(".delete-image");

    input.addEventListener("change", () => {
        if (!input.files.length) {
            return;
        }

        const nextForm = imageForms[index + 1];

        if (nextForm) {
            nextForm.hidden = false;
        }
    });

    deleteButton.addEventListener("click", () => {
        input.value = "";
        form.hidden = true;
    });
});
