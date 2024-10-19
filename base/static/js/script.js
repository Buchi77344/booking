//Script to show showDrop onclick
const categoryContainer = document.querySelector(".category-container")
const categoryHighlight = document.querySelectorAll(".category-highlight")
const destinationCategoryHighlight = document.querySelector(".destination-container .category-highlight")
const mapRegionsWrapper = document.querySelector(".map-regions-wrapper")
const dateWrapper = document.querySelector(".date-wrapper")
// const checkinHighlight = document.querySelector(".checkin.date-wrapper .category-highlight")
const dateCategoryHighlight = document.querySelector(".date-wrapper .category-highlight")
const choiceCategoryHighlight = document.querySelector(".category_choice-wrapper .category-highlight")
const dateContentContainer = document.querySelector(".date-content-container")
const guestCatHihglight = document.querySelector(".guest-container .category-highlight")
const guestShowDrop = document.querySelector(".guest-container .show-drop")
const destinationInput = document.querySelectorAll(".destination-input")
const calNext = document.querySelectorAll(".cal-next")
const calPrev = document.querySelectorAll(".cal-prev")
const detailsDateCategory = document.querySelector(".date.list-group-item .highlight")
const detailsGuestCategory = document.querySelector(".guest.list-group-item .highlight")
const checkoutGuestHighlight = document.querySelector(".checkout-guest-val-div .highlight")
const addPhoneOverlay = document.querySelector(".phone-add-btn")
const removeIconDiv = document.querySelector(".remove-icon-div")
const phoneOverlay = document.querySelector(".phone-number-overlay")

let isLiked;

if(addPhoneOverlay){
    addPhoneOverlay.addEventListener("click", function(){
        phoneOverlay.classList.add("reveal")
    })

    removeIconDiv.addEventListener("click", function(){
        phoneOverlay.classList.remove("reveal")
    })
}


function revealDropFunc(highlightEl, dropEl){
    
    document.addEventListener("click", function(event){
        let parentEl = document.querySelector(highlightEl)
        if(event.target.closest(highlightEl) == null){
            dropEl.classList.remove("reveal")
            if(parentEl.querySelector(".category-highlight")){
                parentEl.querySelector(".category-highlight").classList.remove("active")
            }
        }
    })
}

if(document.querySelector(".phone-number-select-container")){
    revealDropFunc(".phone-number-select-container, .phone-add-btn", phoneOverlay)

}

document.addEventListener("click", function(event){
    if(event.target.closest("#open-chatbot-modal, .chatbot-modal") == null){
        if(document.querySelector(".chatbot-modal")){
            document.querySelector(".chatbot-modal").style.display = "none"
        }
    }
})

if(document.querySelector(".list-group-item")){
    detailsDateCategory.addEventListener("click", function(){
        let dropEl = document.querySelector(".date.list-group-item .show-drop")
        dropEl.classList.toggle("reveal")
        revealDropFunc(".date.list-group-item", dropEl)
    })

    detailsGuestCategory.addEventListener("click", function(){
        let dropEl = document.querySelector(".guest.list-group-item .show-drop")
        dropEl.classList.toggle("reveal")
        revealDropFunc(".guest.list-group-item", dropEl)
    }) 


}

if(document.querySelector(".checkout-guest-val-div")){
    
    checkoutGuestHighlight.addEventListener("click", function(){
        let dropEl = document.querySelector(".checkout-guest-val-div .show-drop")
        dropEl.classList.toggle("reveal")
        revealDropFunc(".checkout-guest-val-div", dropEl)
    })
}

if(document.querySelector(".show-drop") ){
    if(dateCategoryHighlight){
        dateCategoryHighlight.addEventListener("click", function(){
            dateContentContainer.style.width = `${categoryContainer.clientWidth}px`
            document.querySelector(".date-wrapper .show-drop").classList.toggle("reveal")
            let dropEl = document.querySelector(".date-wrapper .show-drop")
            revealDropFunc(".date-wrapper", dropEl)
        })
    }
    
    window.addEventListener("resize", function(){
        if(dateContentContainer || categoryContainer){
            dateContentContainer.style.width = `${categoryContainer.clientWidth}px`
        }
    })

    if(categoryHighlight){
        categoryHighlight.forEach((el) => {
            el.addEventListener("click", function (){
                document.querySelectorAll(".category-highlight").forEach(el => el.classList.remove("active"))
                this.classList.add("active")
            })
        })
    }

    if(choiceCategoryHighlight){
        choiceCategoryHighlight.addEventListener("click", function(){
            document.querySelector(".category_choice-wrapper .show-drop").classList.toggle("reveal")
            let dropEl = document.querySelector(".category_choice-wrapper .show-drop")
            revealDropFunc(".category_choice-wrapper", dropEl)
        })
    }

    if(guestCatHihglight){
        guestCatHihglight.addEventListener("click", function(){
            guestShowDrop.classList.toggle("reveal")
            revealDropFunc(".guest-container", guestShowDrop)
        })
    }

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

    function mobileGuestSum(){
        let totalGuests = adultGuestCount + childrenGuestCount + infantGuestCount + petGuestCount
        document.querySelector(".guest.accord-search-container .accord-search-val").textContent = `${totalGuests} ${totalGuests < 2 ? 'guest' : 'guests'}`;
        
    }

    function detailsGuestSum(){
        let totalGuests = adultGuestCount + childrenGuestCount + infantGuestCount + petGuestCount
        document.querySelector(".guest.list-group-item .group-item-val").textContent = `${totalGuests} ${totalGuests < 2 ? 'guest' : 'guests'}`;
        document.querySelector(".guest.list-group-item .hide-details-guests").value = `${totalGuests}`;
    }

    function checkoutGuestSum(){
        let totalGuests = adultGuestCount + childrenGuestCount + infantGuestCount + petGuestCount
        document.querySelector(".checkout-guests-val").textContent = `${totalGuests} ${totalGuests < 2 ? 'guest' : 'guests'}`;
        // document.querySelector(".guest.list-group-item .hide-details-guests").value = `${totalGuests}`;
    }

    //Add Guest functionality
    if(document.querySelectorAll(".guest-control-container")){
        let adultGuestBox = document.querySelectorAll(".adult.guest-control-container")
        adultGuestBox.forEach(el => el.querySelector(".add-guest").addEventListener("click", function(){
            adultGuestCount = increaseGuestCount(el, adultGuestCount, 14)
            if(el.closest(".accord-search-container .show-drop")){
                mobileGuestSum()
            }else if(el.closest(".guest.list-group-item .show-drop")){
                detailsGuestSum()
            }else if(el.closest(".checkout-guest-val-div .show-drop")){
                checkoutGuestSum()
            }else{
                updateGuestSum()
            }
        }))
    
        adultGuestBox.forEach(el => el.querySelector(".reduce-guest").addEventListener("click", function(){
            adultGuestCount = decreaseGuestCount(el, adultGuestCount)
            if(el.closest(".accord-search-container .show-drop")){
                mobileGuestSum()
            }else if(el.closest(".guest.list-group-item .show-drop")){
                detailsGuestSum()
            }else if(el.closest(".checkout-guest-val-div .show-drop")){
                checkoutGuestSum()
            }else{
                updateGuestSum()
            }
        }))
    
        let childrenGuestBox = document.querySelectorAll(".children.guest-control-container")
        childrenGuestBox.forEach(el => el.querySelector(".add-guest").addEventListener("click", function(){
            childrenGuestCount = increaseGuestCount(el, childrenGuestCount, 5)
            if(el.closest(".accord-search-container .show-drop")){
                mobileGuestSum()
            }else if(el.closest(".guest.list-group-item .show-drop")){
                detailsGuestSum()
            }else if(el.closest(".checkout-guest-val-div .show-drop")){
                checkoutGuestSum()
            }else{
                updateGuestSum()
            }
        }))
    
        childrenGuestBox.forEach(el => el.querySelector(".reduce-guest").addEventListener("click", function(){
            childrenGuestCount = decreaseGuestCount(el, childrenGuestCount)
            if(el.closest(".accord-search-container .show-drop")){
                mobileGuestSum()
            }else if(el.closest(".guest.list-group-item .show-drop")){
                detailsGuestSum()
            }else if(el.closest(".checkout-guest-val-div .show-drop")){
                checkoutGuestSum()
            }else{
                updateGuestSum()
            }
        }))
    
    
        let infantGuestBox = document.querySelectorAll(".infant.guest-control-container")
        infantGuestBox.forEach(el => el.querySelector(".add-guest").addEventListener("click", function(){
            infantGuestCount = increaseGuestCount(el, infantGuestCount, 5)
            // updateGuestSum()
            if(el.closest(".accord-search-container .show-drop")){
                mobileGuestSum()
            }else if(el.closest(".guest.list-group-item .show-drop")){
                detailsGuestSum()
            }else if(el.closest(".checkout-guest-val-div .show-drop")){
                checkoutGuestSum()
            }else{
                document.querySelector(".guest-container .infant-guest").textContent = `${infantGuestCount} ${infantGuestCount < 2 ? 'infant' : 'infants'},`;
            }
    
        }))
    
        infantGuestBox.forEach(el => el.querySelector(".reduce-guest").addEventListener("click", function(){
            infantGuestCount = decreaseGuestCount(el, infantGuestCount)
            // updateGuestSum()
            if(el.closest(".accord-search-container .show-drop")){
                mobileGuestSum()
            }else if(el.closest(".guest.list-group-item .show-drop")){
                detailsGuestSum()
            }else if(el.closest(".checkout-guest-val-div .show-drop")){
                checkoutGuestSum()
            }else{
                document.querySelector(".guest-container .infant-guest").textContent = `${infantGuestCount} ${infantGuestCount < 2 ? 'infant' : 'infants'},`;
            }
    
        }))
    
    
        let petGuestBox = document.querySelectorAll(".pet.guest-control-container")
        petGuestBox.forEach(el => el.querySelector(".add-guest").addEventListener("click", function(){
            petGuestCount = increaseGuestCount(el, petGuestCount, 5)
            // updateGuestSum()
        
            if(el.closest(".accord-search-container .show-drop")){
                mobileGuestSum()
            }else if(el.closest(".guest.list-group-item .show-drop")){
                detailsGuestSum()
            }else if(el.closest(".checkout-guest-val-div .show-drop")){
                checkoutGuestSum()
            }else{
                document.querySelector(".guest-container .pet-guest").textContent = `${petGuestCount} ${petGuestCount < 2 ? 'pet' : 'pets'}`;
            }
    
        }))
    
        petGuestBox.forEach(el => el.querySelector(".reduce-guest").addEventListener("click", function(){
            petGuestCount = decreaseGuestCount(el, petGuestCount)
            // updateGuestSum()
            if(el.closest(".accord-search-container .show-drop")){
                mobileGuestSum()
            }else if(el.closest(".guest.list-group-item .show-drop")){
                detailsGuestSum()
            }else if(el.closest(".checkout-guest-val-div .show-drop")){
                checkoutGuestSum()
            }else{
                document.querySelector(".guest-container .pet-guest").textContent = `${petGuestCount} ${petGuestCount < 2 ? 'pet' : 'pets'}`;
            }
    
        }))

    }


    //Search Functionality
    const categoryField = document.querySelector(".category-field")
    if(destinationCategoryHighlight){
        destinationCategoryHighlight.addEventListener("click", function(){
            mapRegionsWrapper.classList.toggle("reveal")
            categoryField.focus()
            revealDropFunc(".destination-container", mapRegionsWrapper)
        })
        const locationList = document.querySelector(".location-list")
        const searchFormBtn = document.querySelector(".search-form-btn")
        let list =  ""
        destinationInput.forEach(el => el.addEventListener("input", async function(){
            const parent = el.closest(".show-drop")
    
            if(el.closest(".show-drop")){
                parent.querySelector(".location-list").innerHTML = ""
            }else{
                console.log(locationList)
                locationList.innerHTML = ""
            }
    
            list = ""
    
            const query = this.value;
            const apiKey = "pk.0c362d8fcfc2daf1ed669ae23cd5a641"
           
            const response = await fetch(`https://us1.locationiq.com/v1/autocomplete.php?key=${apiKey}&q=${query}&format=json`);
            const data = await response.json();
            
    
            data.forEach(place => {
                // const li = document.createElement('li');
                // li.textContent = place.display_name;
                // locationList.appendChild(li);
                list += `
                    <li class = "location-list-item flex gp-20"> 
                        <span class = "destination-icon">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#f2f2f2">
                                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                                <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                                <g id="SVGRepo_iconCarrier"> 
                                    <path d="M12 21C15.5 17.4 19 14.1764 19 10.2C19 6.22355 15.866 3 12 3C8.13401 3 5 6.22355 5 10.2C5 14.1764 8.5 17.4 12 21Z" stroke="#f2f2f2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> 
                                    <path d="M12 12C13.1046 12 14 11.1046 14 10C14 8.89543 13.1046 8 12 8C10.8954 8 10 8.89543 10 10C10 11.1046 10.8954 12 12 12Z" stroke="#f2f2f2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> 
                                </g>
                            </svg>
                        </span>
    
                        <span class = "location-item-text">${place.display_name}</span>
                    </li>
                `
                
            });
    
            if(el.closest(".show-drop")){
                parent.querySelector(".location-list").innerHTML = list
            }else{
                locationList.innerHTML = list
            }
            
            document.querySelectorAll(".map-regions-wrapper .location-list-item").forEach(list => {
                list.addEventListener("click", function(){
                    document.querySelector(".category-field").value = this.querySelector(".location-item-text").textContent
                })
            })
    
            document.querySelectorAll(".mob_location-container .location-list-item").forEach(list => {
                list.addEventListener("click", function(){
                    document.querySelector(".location_mob-input").value = this.querySelector(".location-item-text").textContent
                })
            })
        }))
    }
    
    const mobileCategoryContainer = document.querySelector(".mobile.category-container")
    const mobileSearchContainer = document.querySelector(".mobile-search-container")
    const accordSearchField = document.querySelectorAll(".accord-search-field")
    const accordSearchContainer = document.querySelectorAll(".accord-search-container")
    const cancelSearch = document.querySelector(".cancel-search")

    if(mobileCategoryContainer){
        mobileCategoryContainer.addEventListener("click", function(event){
            mobileSearchContainer.classList.add("reveal")
            if(event.target.closest(".mobile.category-container") == null || event.target.closest(".mobile-search-container") == null){
                // dropEl.classList.remove("reveal")
                mobileCategoryContainer.querySelector(".category-highlight").classList.remove("active")
            }
            document.body.classList.add("over-hidden")
        })
    
        if(document.querySelector(".cancel-search")){
            cancelSearch.addEventListener("click", function(){
                mobileSearchContainer.classList.remove("reveal")
                document.body.classList.remove("over-hidden")
        
            })
        }
    
    
        accordSearchContainer.forEach(accordCon => {
            // accord.addEventListener("click", function(){
            //     this.querySelector(".show-drop").classList.toggle("reveal")
            // })
    
            
            accordCon.querySelector(".accord-search-field").addEventListener("click", function(){
                document.querySelectorAll(".accord-search-container .show-drop").forEach(el => el.classList.remove("reveal"))
                accordCon.querySelector(".show-drop").classList.toggle("reveal")
            })
    
        })
    
        const categoryChoiceItem = document.querySelectorAll(".category_choice-wrapper .category_choice-item")
        const mobileCategoryChoiceItem = document.querySelectorAll(".accord-search-container .category_choice-item")
    
        function inputItemVal(itemEl, valElstr){
            itemEl.forEach(el => {
                el.addEventListener("click", function(){
                    console.log(el.closest(".accord-search-val"))
                    if(el.closest(".accord-search-val")){
                        document.querySelector(valElstr).value = el.textContent
                    }
                    document.querySelector(valElstr).value = el.textContent
                    // console.log(document.querySelector(valElstr))
                })
            })
        }
    
        function categoryInputLap(){
            categoryChoiceItem.forEach(el => {
                el.addEventListener("click", function(){
                    // console.log("hi")
                    document.querySelector(".category_choice-wrapper .category-field").value = el.textContent
                    // console.log(document.querySelector(valElstr))
                })
            })
        }
    
        // inputItemVal(categoryChoiceItem, ".category_choice-wrapper .category-field")
        categoryInputLap()
        inputItemVal(mobileCategoryChoiceItem, ".choice.accord-search-container .accord-search-val")

    }
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
    const laptopCalendarContainer = document.querySelector('.laptop.calendar-container');
    const mobileCalendarContainer = document.querySelector('.mobile.calendar-container');
    const calendarContainer = document.querySelectorAll('.calendar-container');
    // Function to render a single month's calendar
    const calendarContainers = document.querySelectorAll('.calendar-container');

    // Function to render a single month's calendar
    function renderMonthCalendar(month, year) {
        // Create the calendar for each container
        calendarContainers.forEach(container => {
            const calendar = document.createElement('div');
            calendar.classList.add('calendar');
    
            // Create the month header (Month Name and Year)
            const header = document.createElement('div');
            header.classList.add('calendar-header');
            header.innerHTML = `<h3>${new Date(year, month).toLocaleString('default', { month: 'long' })} ${year}</h3>`;
            calendar.appendChild(header);
    
            // Create weekdays
            const weekdayContainer = document.createElement('div');
            weekdayContainer.classList.add('weekdays-container');
            const weekdaysNames = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];
            weekdaysNames.forEach(weekdayN => {
                const listEl = `<span class="weekday-span">${weekdayN}</span>`;
                weekdayContainer.innerHTML += listEl;
            });
            calendar.appendChild(weekdayContainer);
    
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
    
            // Append the calendar to the current container
            container.appendChild(calendar);
    
            // Add click event for days (same logic as before)
            calendar.querySelectorAll(".day-cell").forEach(day => {
                day.addEventListener("click", function () {
                    document.querySelectorAll(".day-cell").forEach(el => el.classList.remove("active"));
                    this.classList.add("active");
                    let monthYear = calendar.querySelector(".calendar-header").textContent;
                    let [calMonth, calYear] = monthYear.split(" ");
                    let dateVal = this.textContent;
                    console.log(day.closest(".accord-search-container .show-drop"))
                    let mobileBool = day.closest(".accord-search-container .show-drop")
                    let detailsBool = day.closest(".date.list-group-item .show-drop")
                    if(mobileBool){
                        document.querySelector(".date.accord-search-container .accord-search-val").textContent = `${calMonth.slice(0, 3)} ${dateVal} ${calYear}`;
                    }else if(detailsBool){
                        document.querySelector(".date.list-group-item .group-item-val").textContent = `${calMonth.slice(0, 3)} ${dateVal} ${calYear}`;
                        document.querySelector(".date.list-group-item .hide-details-date").value = `${calMonth.slice(0, 3)} ${dateVal} ${calYear}`;
                        console.log(document.querySelector(".date.list-group-item .hide-details-date").value)
                
                    }else{
                        document.querySelector(".date-wrapper .category-val").textContent = `${calMonth.slice(0, 3)} ${dateVal} ${calYear}`;
                    }
                });
            });

            let calendarEl = document.querySelectorAll(".calendar")

            // Function to handle next slide for both containers
            function handleCalNext(container) {
                let nextCalEl = container.scrollLeft + container.querySelector('.calendar').clientWidth;
                container.scrollLeft = nextCalEl;
            }

            // Function to handle previous slide for both containers
            function handleCalPrev(container) {
                let prevCalEl = container.scrollLeft - container.querySelector('.calendar').clientWidth;
                container.scrollLeft = prevCalEl;
            }

            // Add event listeners for both laptop and mobile calendars
            calNext.forEach((el) => {
                el.addEventListener("click", () => {
                    if (el.closest('.laptop.show-drop')) {
                        handleCalNext(laptopCalendarContainer);
                    } else if (el.closest('.mobile.show-drop')) {
                        handleCalNext(mobileCalendarContainer);
                    }
                });
            });

            calPrev.forEach((el) => {
                el.addEventListener("click", () => {
                    if (el.closest('.laptop.show-drop')) {
                        handleCalPrev(laptopCalendarContainer);
                    } else if (el.closest('.mobile.show-drop')) {
                        handleCalPrev(mobileCalendarContainer);
                    }
                });
            });
        });


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
        calendarContainer.forEach(el => el.innerHTML = '')  // Clear the calendar
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
    threshold : 0.5
}

const observer = new IntersectionObserver(observerCallback, options)
const observedElements = document.querySelectorAll(".util-card, .util-card-head, .footer-section")
observedElements.forEach(el => el.classList.add("animate"))
observedElements.forEach(el => el.classList.add("trans"))
observedElements.forEach(el => observer.observe(el))

if(document.querySelector(".mobile.hamburger")){
    let mobileHamburger = document.querySelector(".mobile.hamburger")
    let mobileNav = document.querySelector(".mobile.nav-links-container")
    let overlayEl = document.querySelector(".overlay")
    mobileHamburger.addEventListener("click", function(){
        overlayEl.classList.toggle("visible")
        document.body.classList.toggle("over-hidden")
        mobileNav.classList.toggle("slideIn")
    })
}

console.log(document.querySelector(".host-info-div .hamburger"))

if(document.querySelector(".host-info-div .hamburger")){
    let hamburger = document.querySelector(".host-info-div .hamburger")
    let sideBar = document.querySelector(".host-sidebar")
    hamburger.addEventListener("click", function(){
        sideBar.classList.toggle("slideIn")
    })
}

function dragDropFunc(){
    if(document.querySelector(".upload_dropover")){
        const dropOverEl = document.querySelector(".upload_dropover")
        const uploadInput = document.querySelector("#upload-input")

        let droppedFiles = []
        ['dragover', 'dragenter'].forEach((eventName) => {
            dropOverEl.addEventListener(eventName, function(event){
                event.preventDefault()
                dropOverEl.classList.add("over")
            })
        })

        ['drop', 'dragleave'].forEach((eventName) => {
            dropOverEl.addEventListener(eventName, function(event){
                event.preventDefault()
                dropOverEl.classList.remove("over")
            })
        })

        dropOverEl.addEventListener("drop", function(event){
            event.preventDefault()

            let files = event.dataTransfer.files
        
            handleFilesFunc(files)

        })

        uploadInput.addEventListener("change", function(event){
            let files = event.target.files

            handleFilesFunc(files)
        })

        function handleFilesFunc(files){
            const dataTransfer = new DataTransfer()

            Array.from(files).forEach((file) => {
                if(file.type.startsWith("/image")){
                    droppedFiles.push(file)
                    console.log(droppedFiles)
                    dataTransfer.items.add(file)
                }

                uploadInput.files = dataTransfer.files  
            })
        }
    }
}

dragDropFunc()

if (document.querySelector(".add-watchlist-btn")) {
    let cartBtn = document.querySelectorAll(".add-watchlist-btn");

    cartBtn.forEach((btn, index) => {
        // Check if the state exists in localStorage; if not, initialize it as 'false' (i.e., not liked)
        if (localStorage.getItem(`watchlist-btn-${index}`) === null) {
            localStorage.setItem(`watchlist-btn-${index}`, 'false');
        }

        // Retrieve the state from localStorage
        let isLiked = localStorage.getItem(`watchlist-btn-${index}`) === 'true';
        
        // Update button text based on saved state
        btn.querySelector(".price-span").textContent = isLiked ? "Remove cart" : "Add to cart";

        btn.addEventListener("click", (e) => {
            e.preventDefault();

            // Toggle the liked state
            isLiked = !isLiked;

            // Update button text based on the new state
            btn.querySelector(".price-span").textContent = isLiked ? "Remove cart" : "Add to cart";

            // Save the new state in localStorage
            localStorage.setItem(`watchlist-btn-${index}`, isLiked);
        });
    });
}

if(document.querySelector(".comment-form")){
    let commentForm = document.querySelector(".comment-form")
    let reviewContainer = document.querySelector(".review-container")
    commentForm.addEventListener("submit", function(e){
        e.preventDefault()
        let nameInput = document.querySelector(".comment-form input#name").value
        let messageInput = document.querySelector(".comment-form textarea#message").value
        let ratingInput = document.querySelector("input[name = 'rating']:checked").value
        if(nameInput && messageInput && ratingInput){
            const newReview = document.createElement('div')
            newReview.classList.add("review-item")
            let starRating = getStarRating(ratingInput)
            newReview.innerHTML = `
                <h3 class = "name-review_item">${nameInput}</h3>
                ${starRating}
                <p>${messageInput}</p>
            `
            reviewContainer.appendChild(newReview)
        }
    })

    function getStarRating(rating){
        let star = ""
        for(let i = 1; i <= 5; i++){
            if(i <= rating){
                star += `<span class="star gold">★</span>`
            }else{
                star += `<span class= "star gray">★</span>`
            }
        }

        return star
    }
}

if(document.querySelector(".chat-cta")){
    let chatCta = document.querySelector(".chat-cta")
    let chatBoxContainer = document.querySelector(".chat-box-container")
    chatCta.addEventListener("click", function(){
        chatBoxContainer.classList.toggle("shrink")
    })

    // Get DOM elements
    const chatBox = document.querySelector('.chat-main');
    const messageInput = document.querySelector('.chat-input');
    const sendBtn = document.querySelector('.submit-chat');

    // Function to add a message to the chat box
    function addMessage(message, isUser = true) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.textContent = isUser ? `You: ${message}` : `Bot: ${message}`;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto scroll to bottom
    }

    // Function to handle message sending
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message === '') return; // Don't send empty messages
        addMessage(message); // Add user's message
        messageInput.value = ''; // Clear input field
        respondToMessage(message); // Simulate bot response
    }

    // Simulate a bot response
    function respondToMessage(userMessage) {
        setTimeout(() => {
            const botResponse = `I received your message: "${userMessage}"`; // Example response
            addMessage(botResponse, false); // Add bot's response
        }, 1000); // Delay to mimic typing
    }

    // Event listener for the Send button
    sendBtn.addEventListener('click', sendMessage);

    // Allow sending messages by pressing Enter
    messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault()
            sendMessage();
        }
    });

    let initialMessage = `Hi there, my name is agent`
    addMessage(initialMessage, false)

}
// if(document.querySelector(".faq-content-item")){
//     let faqItemHead = document.querySelectorAll(".faq-item-head")
//     let faqItemContent = document.querySelectorAll(".faq-item-content")

//     faqItemHead.forEach((el, index) => {
//         el.onclick = function(){    
//             removeOtherAccordions(index)
//             faqItemContent[index].classList.toggle("lengthen")
//         }
//     })

//     function removeOtherAccordions(index){
//         faqItemContent.forEach((item, i) => {
//             if(i !== index){
//                 console.log(item)
//                 item.classList.remove("lengthen")
//             }
//         })
//     }
// }