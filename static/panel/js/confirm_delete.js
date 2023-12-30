document.addEventListener('DOMContentLoaded', () => {

    // confirm delete modal
    let form_confirm = document.querySelector('#form_confirm_modal')
    let buttons = document.querySelectorAll("[data-target='#deleteItemModal']");
        buttons.forEach(button => {
            button.addEventListener("click", () => {

                 // extract texts from calling element and replace the modals texts with it
                if (button.dataset.message) {
                    document.getElementById("modal-message").innerHTML = button.dataset.message;
                }
                // extract url from calling element and replace the modals texts with it
                if (button.dataset.url) {
                    form_confirm.action = button.dataset.url;
                }

            })
        });
   let confirmModal = document.getElementById("confirmButtonModal")
    confirmModal.addEventListener('click', () => {
        form_confirm.submit();
    });

    // image observation modal
    
});