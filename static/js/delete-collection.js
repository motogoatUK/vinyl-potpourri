/**
 * delete-collection confirmation modal
 */
// Wait for DOM
document.addEventListener("DOMContentLoaded", function() {
    const deleteButtons = document.getElementsByClassName('btn-delete');
    const modalContent = document.getElementById("modal-content");
    const modalWindow = new bootstrap.Modal(document.getElementById('modalWindow'));
    const modalConfirm = document.getElementById("modalConfirm");

    for (let button of deleteButtons) {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            let message = "Are you sure you want to delete this collection?<br>";
            message += "All records in "+ modalContent.innerText + " will be deleted";
            /* set modal button link */
            modalConfirm.href = e.target.href;
            /* set modal title, content and button text and show the modal */
            modalConfirm.innerText = "Confirm Delete";
            modalContent.innerHTML = message;
            modalWindow.show();
        })
    }
})