/**
* delete-record modal to confirm potential deletion
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
            /* set modal title, content and button text and show the modal */
            modalConfirm.innerText = "Delete";
            modalContent.innerHTML = "Are you sure you want to delete this record?<br>" + button.dataset.record;
            modalWindow.show();
        });
    };
});