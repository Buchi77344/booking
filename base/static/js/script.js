//Script to show showDrop onclick
const categoryContainer = document.querySelector(".category-container")
const destinationCategoryHighlight = document.querySelector(".destination-container .category-highlight")
const mapRegionsWrapper = document.querySelector(".map-regions-wrapper")
const dateWrapper = document.querySelector(".date-wrapper")
const checkinHighlight = document.querySelector(".checkin.date-wrapper .category-highlight")
const dateCategoryHighlight = document.querySelector(".date-wrapper .category-highlight")
const dateContentContainer = document.querySelector(".date-content-container")
const guestCatHihglight = document.querySelector(".guest-container .category-highlight")
const guestShowDrop = document.querySelector(".guest-container .show-drop")
let isLiked;

function revealDropFunc(highlightEl, dropEl){
    
    document.addEventListener("click", function(event){
        if(event.target.closest(highlightEl) == null){
            dropEl.classList.remove("reveal")
        }
    })
}

if(document.querySelector(".category-container")){
    dateCategoryHighlight.addEventListener("click", function(){
        dateContentContainer.style.width = `${categoryContainer.clientWidth}px`
        document.querySelector(".date-wrapper .show-drop").classList.toggle("reveal")
        let dropEl = document.querySelector(".date-wrapper .show-drop")
        revealDropFunc(".date-wrapper", dropEl)
    })
    
    window.addEventListener("resize", function(){
        dateContentContainer.style.width = `${categoryContainer.clientWidth}px`
    })

    guestCatHihglight.addEventListener("click", function(){
        guestShowDrop.classList.toggle("reveal")
        revealDropFunc(".guest-container", guestShowDrop)
    })
    let adultGuestCount = 0
    let childrenGuestCount = 0
    let infantGuestCount = 0
    let petGuestCount = 0
    function increaseGuestCount(parentEl, guestCount, num){
     
        if(guestCount < num){
            guestCount = guestCount + 1
            parentEl.querySelector(".guest-count").textContent = guestCount
        }
         
        return guestCount
    }

    function decreaseGuestCount(parentEl, guestCount){
        if(guestCount > 0){
            guestCount--
            parentEl.querySelector(".guest-count").textContent = guestCount
        }

        return guestCount
    }

    function updateGuestSum() {
        let totalGuests = adultGuestCount + childrenGuestCount;
        document.querySelector(".guest-container .category-val").textContent = `${totalGuests} ${totalGuests < 2 ? 'guest' : 'guests'},`;
    }

    let adultGuestBox = document.querySelector(".adult.guest-control-container")
    adultGuestBox.querySelector(".add-guest").addEventListener("click", function(){
        adultGuestCount = increaseGuestCount(adultGuestBox, adultGuestCount, 14)
        updateGuestSum()
    })

    adultGuestBox.querySelector(".reduce-guest").addEventListener("click", function(){
        adultGuestCount = decreaseGuestCount(adultGuestBox, adultGuestCount)
        updateGuestSum()
    })

    let childrenGuestBox = document.querySelector(".children.guest-control-container")
    childrenGuestBox.querySelector(".add-guest").addEventListener("click", function(){
        childrenGuestCount = increaseGuestCount(childrenGuestBox, childrenGuestCount, 5)
        updateGuestSum()
    })

    childrenGuestBox.querySelector(".reduce-guest").addEventListener("click", function(){
        childrenGuestCount = decreaseGuestCount(childrenGuestBox, childrenGuestCount)
        updateGuestSum()
    })


    let infantGuestBox = document.querySelector(".infant.guest-control-container")
    infantGuestBox.querySelector(".add-guest").addEventListener("click", function(){
        infantGuestCount = increaseGuestCount(infantGuestBox, infantGuestCount, 5)
        updateGuestSum()
        document.querySelector(".guest-container .infant-guest").textContent = `${infantGuestCount} ${infantGuestCount < 2 ? 'infant' : 'infants'},`;

    })

    infantGuestBox.querySelector(".reduce-guest").addEventListener("click", function(){
        infantGuestCount = decreaseGuestCount(infantGuestBox, infantGuestCount)
        updateGuestSum()
        document.querySelector(".guest-container .infant-guest").textContent = `,${infantGuestCount} ${infantGuestCount < 2 ? 'infant' : 'infants'},`;

    })


    let petGuestBox = document.querySelector(".pet.guest-control-container")
    petGuestBox.querySelector(".add-guest").addEventListener("click", function(){
        petGuestCount = increaseGuestCount(petGuestBox, petGuestCount, 5)
        updateGuestSum()
        document.querySelector(".guest-container .pet-guest").textContent = `${petGuestCount} ${petGuestCount < 2 ? 'pet' : 'pets'}`;

    })

    petGuestBox.querySelector(".reduce-guest").addEventListener("click", function(){
        petGuestCount = decreaseGuestCount(petGuestBox, petGuestCount)
        updateGuestSum()
        document.querySelector(".guest-container .pet-guest").textContent = `${petGuestCount} ${petGuestCount < 2 ? 'pet' : 'pets'}`;

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

        calendarContainer.appendChild(calendar)

        // Append the month container to the main calendar container
        let calMonth;
        let calYear;
        let calendarEl = document.querySelectorAll(".calendar")
        calendarEl.forEach(cal => {
            const dayCell = cal.querySelectorAll(".day-cell")   
            dayCell.forEach((day) => {
                day.addEventListener("click", function(){
                    document.querySelectorAll(".day-cell").forEach(el => el.classList.remove("active"))
                    this.classList.add("active")
                    let monthYear = cal.querySelector(".calendar-header").textContent
                    let [calMonth, calYear] = monthYear.split(" ")
                    // console.log(calMonth.slice(0,3))
                    let dateVal = this.textContent
                    console.log(dateVal)

                    document.querySelector(".date-wrapper .category-val").textContent = `${calMonth.slice(0,3)} ${dateVal}`
                })
            })
        })        
            
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
        calendarContainer.innerHTML = ''  // Clear the calendar
        const currentDate = new Date();
        const currentMonth = currentDate.getMonth();  // Get current month (0 = January, 11 = December)
        const currentYear = currentDate.getFullYear(); // Get current year

        renderMonthsFrom(currentMonth, currentYear);  // Render remaining months of the current year
        renderYearCalendarFromStart(currentYear + 1); // Render the next year (from January)
    }

    // Call the function to render the calendar for this and the next year
    renderMultipleYears();

 
}


let profileCta = document.querySelector(".profile-cta")
console.log(profileCta)
let profileDropDown = document.querySelector(".profile-drop-down")
console.log(profileCta)
if(document.querySelector(".profile-cta")){
    profileCta.addEventListener("click", () =>{
        profileDropDown.classList.toggle("visible")
    })
}

// if(document.querySelector(".love-icon")){
//     const loveIcon = document.querySelectorAll(".love-icon-span");


//     loveIcon.forEach(icon => {
//         isLiked = false;
//         icon.addEventListener("click", (e) => {
//             e.preventDefault()
//             if (!isLiked) {
//                 icon.classList.remove("reverse");
//                 icon.classList.add("animate");
//             } else {
//                 icon.classList.remove("animate");
//                 icon.classList.add("reverse");
//             }
//             isLiked = !isLiked;  // Toggle the state
//         });
//     })


// }

//Animation on scroll

const observerCallback = (entries, observer) => {
    entries.forEach((entry, index) => {
        entry.target.style.transitionDelay = `${index * 0.4}s`
        if(entry.isIntersecting){
            entry.target.classList.add("in-view")
            entry.target.classList.remove("animate")
        }else{
            entry.target.classList.remove("in-view")
            entry.target.classList.add("animate")
            
        }
    })
}

const options = {
    root : null,
    threshold : 0.1
}

const observer = new IntersectionObserver(observerCallback, options)
const observedElements = document.querySelectorAll(".util-card, .util-card-head, .footer-section")
observedElements.forEach(el => el.classList.add("animate"))
observedElements.forEach(el => el.classList.add("trans"))
observedElements.forEach(el => observer.observe(el))

if(document.querySelector(".mobile.hamburger")){
    let mobileHamburger = document.querySelector(".mobile.hamburger")
    let mobileNav = document.querySelector(".mobile.nav-links-container")

    mobileHamburger.addEventListener("click", function(){
        mobileNav.classList.toggle("slideIn")
    })
}

if(document.querySelector(".add-watchlist-btn")){
    let cartBtn = document.querySelectorAll(".add-watchlist-btn")
    cartBtn.forEach(btn => {
        isLiked = false;
        console.log(!isLiked)
        btn.addEventListener("click", (e) => {
            e.preventDefault()
            if (!isLiked) {
                btn.querySelector(".price-span").textContent = "Remove cart"
            }else{
                btn.querySelector(".price-span").textContent = "Add to cart"
            }

            isLiked = !isLiked
        }) 
    
    })
}