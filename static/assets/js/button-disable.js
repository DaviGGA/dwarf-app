const postButton = document.querySelector('[data-button]')


textarea.addEventListener('keyup', e => {
    if (e.target.value.length > 0) {
        postButton.classList.remove("disabled")
        console.log('botao lig')
    }

    if (e.target.value.length <= 0) {
        postButton.classList.add("disabled")
        console.log('botao des')
    }
})