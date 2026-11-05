//Christina Rusu

let modalTimeoutID;

function purseModal(bagId, itemData) {
    
    clearTimeout(modalTimeoutID); 

    const modal = document.getElementById("info-modal");
    
    // 2. pull all purse details to display

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

    const buybtn = document.getElementById('buybtn');
    if (buybtn) {
        buybtn.href = `/buy/${bagId}`;
    }
}

//Modal responsible for displaying user credential messages 
function toggleModal(message) {
    const modal = document.getElementById("success-modal");
    const modalContent = document.getElementById("modal-text");

    modalContent.textContent = message;
    modal.style.display = "flex";

    //hide message after 5 seconds
    modalTimeoutID = setTimeout(() => {
        modal.style.display = "none";
    }, 5000);
}

// Function to close any modal window that pops up
function closeModal() {
    const modal = document.getElementById("success-modal");
    modal.style.display = "none";
}

function closePurseModal() {
    const modal = document.getElementById("info-modal");
    modal.style.display = "none";
}

// Similar as toggleModal, just with no time limit so user can see purse info for longer
function buyModal(message) {
    const modal = document.getElementById("success-modal");
    const modalContent = document.getElementById("modal-text");

    modalContent.textContent = message;
    modal.style.display = "flex";

    //hide message after 5 seconds
    clearTimeout(modalTimeoutID); 
}