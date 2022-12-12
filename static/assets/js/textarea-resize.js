const textarea = document.querySelector('.post-write-input')

textarea.addEventListener("keyup",e => {
    let scHeigtht = e.target.scrollHeight;
    textarea.style.height = `${scHeigtht}px`
    console.log(scHeigtht)
    }) 


textarea.addEventListener("focusout", e => {
    textarea.style.height = "58px"
})

