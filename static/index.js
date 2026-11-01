//Christina Rusu

let modalTimeoutID;

function purseModal(itemData) {
    
    clearTimeout(modalTimeoutID); 

    const modal = document.getElementById("info-modal");
    
    // 2. Select all your specific modal content slots
    const modalImg = document.getElementById("modal-img");
    const modalName = document.getElementById("modal-name");
    const modalColor = document.getElementById("modal-color");
    const modalSerial = document.getElementById("modal-serial");
    const modalPrice = document.getElementById("modal-price");


    modalImg.src = itemData.img;
    modalName.textContent = itemData.name;
    modalColor.textContent = itemData.color;
    modalSerial.textContent = itemData.serial;
    modalPrice.textContent = itemData.price;

    modal.style.display = "flex";
}

function toggleModal(message) {
    const modal = document.getElementById("success-modal");
    const modalContent = document.getElementById("modal-text");

    modalContent.textContent = message;
    modal.style.display = "flex";

    //hide message after 5 seconds
    timeout = setTimeout(() => {
        modal.style.display = "none";
    }, 5000);
}

function closeModal() {
    const modal = document.getElementById("success-modal");
    modal.style.display = "none";
}

function closePurseModal() {
    const modal = document.getElementById("info-modal");
    modal.style.display = "none";
}
