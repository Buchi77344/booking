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
    
    // document.addEventListener("click", function(event){
    //     if(event.target.closest(dropElStr) == null){
    //         dropEl.classList.remove("reveal")
    //     }
    // })
}

if(document.querySelector(".category-container")){
    revealDropFunc(destinationCategoryHighlight, mapRegionsWrapper, ".destination-container .category-highlight")
    revealDropFunc(dateCategoryHighlight, dateContentContainer, ".date-wrapper .category-highlight")
    
    dateCategoryHighlight.addEventListener("click", function(){
        dateWrapper.classList.add("static-pos")
        categoryContainer.classList.add("relative-pos")
        dateContentContainer.style.width = `${categoryContainer.clientWidth}px`
    
    })

    window.addEventListener("resize", function(){
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

if(document.querySelector(".calendar-container")){
    const calendarContainer = document.querySelector('.calendar-container');
    const dayCell = document.querySelectorAll(".day-cell")
    // Function to render a single month's calendar
    function renderMonthCalendar(month, year) {
        const calendar = document.createElement('div');
        calendar.classList.add('calendar');

        // Create the month header (Month Name and Year)
        const header = document.createElement('div');
        header.classList.add('calendar-header');
        header.innerHTML = `<h3>${new Date(year, month).toLocaleString('default', { month: 'long' })} ${year}</h3>`;
        calendar.appendChild(header);

        //Create weekdays 
        const weekdayContainer = document.createElement("div")
        weekdayContainer.classList.add("weekdays-container")
        const weekdaysNames = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']
        let listEl;
        weekdaysNames.forEach((weekdayN) => {
           listEl = `
                <span class="weekday-span">${weekdayN}</span>
            `
            weekdayContainer.innerHTML += listEl
            calendar.appendChild(weekdayContainer);
        })

        // Create the days grid
        const daysContainer = document.createElement('div');
        daysContainer.classList.add('days-container');
        calendar.appendChild(daysContainer);

        // Get the first day of the month and the total number of days
        const firstDayOfMonth = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        // Add empty cells for days before the 1st of the month
        for (let i = 0; i < firstDayOfMonth; i++) {
            const emptyCell = document.createElement('div');
            emptyCell.classList.add('empty-cell');
            daysContainer.appendChild(emptyCell);
        }

        // Add the days of the month
        for (let i = 1; i <= daysInMonth; i++) {
            const dayCell = document.createElement('div');
            dayCell.classList.add('day-cell');
            dayCell.textContent = i;
            daysContainer.appendChild(dayCell);
        }

        // Append the month container to the main calendar container
        calendarContainer.appendChild(calendar);
    }

    // Function to render months starting from a given month and year
    function renderMonthsFrom(month, year) {
        // Render months from the current year starting from the current month
        for (let i = month; i < 12; i++) {
            renderMonthCalendar(i, year);
        }
    }

    // Function to render a full year from January
    function renderYearCalendarFromStart(year) {
        for (let month = 0; month < 12; month++) {
            renderMonthCalendar(month, year);
        }
    }

    // Clear the calendar container and render for two years (starting from the current month)
    function renderMultipleYears() {
        calendarContainer.innerHTML = '';  // Clear the calendar
        const currentDate = new Date();
        const currentMonth = currentDate.getMonth();  // Get current month (0 = January, 11 = December)
        const currentYear = currentDate.getFullYear(); // Get current year

        renderMonthsFrom(currentMonth, currentYear);  // Render remaining months of the current year
        renderYearCalendarFromStart(currentYear + 1); // Render the next year (from January)
    }

    // Call the function to render the calendar for this and the next year
    renderMultipleYears();
    console.log(dayCell)
    dayCell.forEach((day) => {
        day.addEventListener("click", function(){
            document.querySelectorAll(".day-cell").forEach(el => el.classList.remove("active"))
            this.classList.add("active")
            console.log(this)
        })
    })
}
