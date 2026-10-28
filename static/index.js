//Christina Rusu

function toggleModal(message) {
    const modal = document.getElementById("success-modal");
    const modalContent = document.getElementById("modal-text");

    modalContent.textContent = message;
    modal.style.display = "flex";

    //hide message after 5 seconds
    setTimeout(() => {
        modal.style.display = "none";
    }, 5000);
}

function closeModal() {
    const modal = document.getElementById("success-modal");
    modal.style.display = "none";
}