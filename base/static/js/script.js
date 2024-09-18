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

