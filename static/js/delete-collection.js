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
            /* set modal button link */
            modalConfirm.href = e.target.href;
            let btnMessage = `Are you sure you want to delete this "${button.dataset.collection}" collection?<br>`;
            btnMessage += "<br><p>All records in this collection will be removed</p>";
            btnMessage += `<p>Edit the records and change their collection, if required before deleting "${button.dataset.collection}".</p>`;
            /* set modal title, content and button text and show the modal */
            modalConfirm.innerText = "Confirm Delete";
            modalContent.innerHTML = btnMessage;
            modalWindow.show();
        });
    };
});