// const dropdownContent = document.querySelector(".dropdown-content")
const dropdownButton = document.querySelectorAll(".drop-btn")


dropdownButton.forEach( b => {
    b.addEventListener('click', function() {
       const dropdownContent = b.parentNode.querySelector(".dropdown-content")
       dropdownContent.classList.toggle("show")    
    })

    
})


