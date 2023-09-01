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
// Function to iterate through cards in the flash session page


// SHOW SUCCESS MODAL --- TODO






