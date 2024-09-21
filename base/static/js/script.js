//Script to show showDrop onclick
const categoryContainer = document.querySelector(".category-container")
const destinationCategoryHighlight = document.querySelector(".destination-container .category-highlight")
const mapRegionsWrapper = document.querySelector(".map-regions-wrapper")
const dateWrapper = document.querySelector(".date-wrapper")
const dateCategoryHighlight = document.querySelector(".date-wrapper .category-highlight")
const dateContentContainer = document.querySelector(".date-content-container")

function revealDropFunc(highlightEl, dropEl, dropElStr){
    highlightEl.addEventListener("click", function(){
        dropEl.classList.toggle("reveal")
    })
    
    document.addEventListener("click", function(event){
        if(event.target.closest(dropElStr) == null){
            dropEl.classList.remove("reveal")
        }
    })
}

if(document.querySelector(".category-container")){
    revealDropFunc(destinationCategoryHighlight, mapRegionsWrapper, ".destination-container .category-highlight")
    revealDropFunc(dateCategoryHighlight, dateContentContainer, ".date-wrapper .category-highlight")
    
    dateCategoryHighlight.addEventListener("click", function(){
        dateWrapper.classList.add("static-pos")
        categoryContainer.classList.add("relative-pos")
        dateContentContainer.style.width = `${categoryContainer.clientWidth}px`
    
    })
}

if(document.querySelector(".form-page")){
    const inputs = document.querySelectorAll(".otp-input input")
    
    inputs.forEach((input, index) => {
        input.addEventListener("input", () => {
            if(input.value.length === 1 && index < inputs.length - 1){
                inputs[index + 1].focus()
            }
        })
    
        input.addEventListener('keydown', (event) => {
            if (event.key === 'Backspace' && input.value === '' && index > 0) {
                inputs[index - 1].focus();
            }
        });
    })
    
    const passwordInput = document.querySelector(".form-input.password")
    const passwordMessage = document.querySelector(".password-message")
    
    function validateMessage(password){
        const regex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/
        return regex.test(password);
    }
    
    passwordInput.addEventListener("input", function(){
        const password = passwordInput.value.trim()
        console.log(validateMessage(password))
        if(!validateMessage(password)){
            passwordMessage.classList.remove("correct")
            passwordMessage.classList.add("incorrect")
        }else{
            passwordMessage.classList.add("correct")
            passwordMessage.classList.remove("incorrect")
        }
    })




}
