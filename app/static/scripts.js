// scripts.js 
// https://getbootstrap.com/docs/4.0/getting-started/javascript/

// FLIP CARDS 
function addCardFlipEventListeners() {
    const flipCards = document.querySelectorAll('.flip-card');

    flipCards.forEach(card => {
        card.addEventListener('click', function () {
            this.classList.toggle('flipped');
        });
    });
}

// Call the addCardFlipEventListeners function when the page loads
window.addEventListener('DOMContentLoaded', addCardFlipEventListeners);


// FLASH SESSIONS
// Function to redirect to the flash session page
// function startFlashSession() {
//     window.location.href = "/flash-session";
// }


// FILTER CARDS BY SELECTED THEMES 
function filterCardsByTheme() {
    const themeCheckboxes = document.querySelectorAll('.theme-checkbox');
    const cardContainers = document.querySelectorAll('.card-container');

    function updateCardDisplay() {
        const selectedThemes = [];
        themeCheckboxes.forEach(checkbox => {
            if (checkbox.checked) {
                selectedThemes.push(checkbox.dataset.theme);
            }
        });

        cardContainers.forEach(container => {
            const cardTheme = container.dataset.theme;
            container.style.display = selectedThemes.includes(cardTheme) ? 'block' : 'none';
        });
    }

    // Add event listener to checkboxes
    themeCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateCardDisplay);
    });

    // Call the updateCardDisplay function initially to show all cards
    updateCardDisplay();
}

// Call the filterCardsByTheme function when the page loads
window.addEventListener('DOMContentLoaded', filterCardsByTheme);



// CURSOR DISPLAY (for the range of theme selection)
const rangeInput = document.getElementById('customRange3');
const rangeValueElement = document.getElementById('rangeValue');

// Add an event listener to the range input to update the displayed value dynamically
rangeInput.addEventListener('input', function () {
    rangeValueElement.innerText = rangeInput.value + " Cards selected";
});


// SHOW SUCCESS MODAL --- TODO






